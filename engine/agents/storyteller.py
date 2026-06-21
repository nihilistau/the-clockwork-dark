"""
Storyteller Agent
=================

GM agent — narrates world, dispatches required skills, passes Evaluator gate.

Version: v0.1.0 [2026-06-20]
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Callable, Optional

from engine.agents.evaluator import EvaluationResult, StorytellerEvaluator
from engine.agents.parsing import parse_storyteller_response  # noqa: F401 (re-export)
from engine.agents.prompts import evaluator_retry_prompt, storyteller_system_prompt
from engine.agents.streaming import ProseStreamGate
from engine.agents.stream_processor import StreamProcessor
from engine.agents.tool_dispatcher import (
    auto_resolve_skill_check,
    execute_tool_calls,
)
from engine.game.engine import GameEngine
from engine.game.plot import PlotFormula
from engine.lmstudio.speculative import speculative_stream
from engine.lore.interceptors import run_pre_interceptors
from engine.lore.manager import get_lore_manager
from engine.media.pipeline import MediaPipeline

logger = logging.getLogger(__name__)


@dataclass
class StorytellerTurnResult:
    """Result of one Storyteller turn."""

    narration: str
    choices: list[dict[str, str]]
    parsed: dict[str, Any]
    tool_receipts: list[dict[str, Any]]
    evaluation: EvaluationResult
    tags_inline: str = ""
    processed_tags: dict[str, list[str]] = field(default_factory=dict)
    media: dict[str, Any] = field(default_factory=dict)
    retries: int = 0
    raw_llm: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "narration": self.narration,
            "choices": self.choices,
            "parsed": self.parsed,
            "tool_receipts": self.tool_receipts,
            "evaluation": self.evaluation.to_dict(),
            "tags_inline": self.tags_inline,
            "processed_tags": self.processed_tags,
            "media": self.media,
            "retries": self.retries,
        }


class StorytellerAgent:
    """
    Orchestrates Storyteller inference, tool execution, and evaluation.

    Args:
        engine: Game engine bound to session state.
        llm_fn: Optional mock/injectable LLM callable(messages) -> str.
        use_speculative: Use draft→refine if True and client available.
    """

    AGENT_ID = "clockwork_storyteller"
    MAX_RETRIES = 1

    def __init__(
        self,
        engine: GameEngine,
        *,
        llm_fn: Optional[Callable[[list[dict[str, Any]]], str]] = None,
        use_speculative: bool = False,
        lms_client: Any = None,
    ) -> None:
        self.engine = engine
        self.llm_fn = llm_fn
        self.use_speculative = use_speculative
        self._client = lms_client
        self._evaluator = StorytellerEvaluator()
        self._media = MediaPipeline()

    def _infer(
        self,
        messages: list[dict[str, Any]],
        *,
        on_delta: Optional[Callable[[str], None]] = None,
    ) -> str:
        """Call LLM via injectable fn, speculative stream, or plain chat.

        When ``on_delta`` is given, narration *prose* is streamed through a
        :class:`ProseStreamGate` (the JSON epilogue is withheld from the client).
        """
        gate = ProseStreamGate(on_delta) if on_delta is not None else None

        if self.llm_fn is not None:
            raw = self.llm_fn(messages)
            if gate is not None:
                gate.feed(raw)
                gate.flush()
            return raw

        from engine.lmstudio.client import get_lms_client

        client = self._client or get_lms_client()
        feed = gate.feed if gate is not None else None

        if self.use_speculative:
            resp = speculative_stream(
                client,
                messages,
                refine_profile="big",
                draft_profile="draft",
                on_delta=feed,
            )
            if gate is not None:
                gate.flush()
            return resp.content

        if gate is not None:
            parts: list[str] = []
            for chunk in client.infer_stream(messages, profile="big"):
                parts.append(chunk)
                gate.feed(chunk)
            gate.flush()
            return "".join(parts)

        from engine.lmstudio.profiles import resolve_profile

        mp = resolve_profile("big")
        return client.chat(
            messages,
            model=mp.model,
            temperature=mp.temperature,
            max_tokens=mp.max_tokens,
        ).content

    def _build_messages(
        self,
        player_action: str,
        *,
        retry_notes: Optional[list[str]] = None,
    ) -> list[dict[str, Any]]:
        state = self.engine.state
        PlotFormula.update_story_pressure(state)
        evil = self.engine.get_evil_snapshot()
        system = storyteller_system_prompt(state, evil)
        system = run_pre_interceptors(
            state,
            system,
            player_action=player_action,
        )
        messages: list[dict[str, Any]] = [
            {"role": "system", "content": system},
            {"role": "user", "content": player_action},
        ]
        if retry_notes:
            messages.append(
                {
                    "role": "user",
                    "content": evaluator_retry_prompt(retry_notes),
                }
            )
        return messages

    def run_turn(
        self,
        player_action: str,
        *,
        on_delta: Optional[Callable[[str], None]] = None,
    ) -> StorytellerTurnResult:
        """
        Execute one Storyteller turn with tools and evaluator retry.

        Args:
            player_action: Player choice or free-text action.
            on_delta: Optional prose-streaming callback (first attempt only);
                the JSON epilogue is withheld from it.

        Returns:
            StorytellerTurnResult with narration and evaluation.
        """
        retries = 0
        retry_notes: list[str] = []
        raw = ""
        parsed: dict[str, Any] = {}
        tool_receipts: list[dict[str, Any]] = []
        processed_tags: dict[str, list[str]] = {}
        evaluation = EvaluationResult(
            overall=0.0,
            tone=0.0,
            lore=0.0,
            no_hallucinated_mechanics=0.0,
            length=0.0,
            valid_json=0.0,
            choices=0.0,
            passed=False,
        )

        while retries <= self.MAX_RETRIES:
            messages = self._build_messages(
                player_action,
                retry_notes=retry_notes if retries else None,
            )
            try:
                # Stream prose only on the first attempt; retries re-infer silently
                # and the final turn_update replaces any streamed (rejected) text.
                raw = self._infer(messages, on_delta=on_delta if retries == 0 else None)
            except Exception as exc:
                logger.warning(
                    "[storyteller] LLM unavailable (operation=run_turn): %s", exc
                )
                raw = (
                    "The forest holds its breath. Smoke drifts from a distant chimney."
                )

            parsed = parse_storyteller_response(raw)
            tool_receipts = execute_tool_calls(
                parsed.get("tool_calls", []),
                self.engine,
            )
            tool_receipts.extend(auto_resolve_skill_check(parsed, self.engine))

            narration = parsed.get("narration", raw)
            tags_inline = parsed.get("tags_inline", "")
            if tags_inline:
                tag_result = StreamProcessor.extract_tags(tags_inline)
                processed_tags = tag_result.all_tags
            else:
                tag_result = StreamProcessor.extract_tags(narration)
                processed_tags = tag_result.all_tags

            lore_query = f"{self.engine.state.location_id} {player_action}"
            lore_chunks = get_lore_manager().search(lore_query, limit=3)
            evaluation = self._evaluator.evaluate(
                narration,
                parsed,
                tool_receipts=tool_receipts,
                lore_snippets=[c.text for c in lore_chunks],
            )

            if evaluation.passed:
                break

            retry_notes = evaluation.notes
            retries += 1

        self.engine.state.turn_number += 1
        self.engine.state.storyteller_mind.patience = max(
            0.0,
            self.engine.state.storyteller_mind.patience - 1.0,
        )

        media_result = self._media.process_storyteller_turn(
            self.engine.state,
            narration=parsed.get("narration", raw),
            processed_tags=processed_tags,
        )

        return StorytellerTurnResult(
            narration=parsed.get("narration", raw),
            choices=parsed.get("choices", []),
            parsed=parsed,
            tool_receipts=tool_receipts,
            evaluation=evaluation,
            tags_inline=parsed.get("tags_inline", ""),
            processed_tags=processed_tags,
            media=media_result.to_dict(),
            retries=retries,
            raw_llm=raw,
        )