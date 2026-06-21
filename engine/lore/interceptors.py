"""
Comms Interceptors (PRE)
========================

Lore injection and awareness gating for agent prompts.

Version: v0.1.0 [2026-06-20]
"""

from __future__ import annotations

import logging
import re
from typing import Any, Optional

from engine.config import get_config
from engine.game.state import GameState
from engine.lore.manager import LoreManager, get_lore_manager

logger = logging.getLogger(__name__)

_SPOILER_TERMS: list[tuple[re.Pattern[str], str]] = [
    (
        re.compile(r"Clockwork Dark", re.IGNORECASE),
        "something wrong in the wheat",
    ),
    (
        re.compile(r"evil_progress", re.IGNORECASE),
        "the village's unease",
    ),
    (
        re.compile(r"\bCONSUMING\b"),
        "the worst of it",
    ),
]


class LoreInjectInterceptor:
    """PRE: inject RAG lore chunks into system context."""

    priority = 6
    name = "LoreInjectInterceptor"

    def __init__(self, manager: Optional[LoreManager] = None) -> None:
        self._manager = manager

    @property
    def manager(self) -> LoreManager:
        return self._manager or get_lore_manager()

    def run_pre(
        self,
        state: GameState,
        system_prompt: str,
        *,
        player_action: str = "",
        limit: int = 3,
    ) -> str:
        """
        Append lore context block when DB has chunks.

        No-op if lore store is empty.
        """
        if self.manager.count() == 0:
            return system_prompt

        query = f"{state.location_id} {player_action} {state.archetype}"
        chunks = self.manager.search(query, limit=limit)
        if not chunks:
            return system_prompt

        lines = [f"- [{c.title}] {c.text}" for c in chunks]
        block = "LORE CONTEXT (canonical — do not contradict):\n" + "\n".join(lines)
        logger.debug(
            "[lore] Injected chunks (operation=run_pre, count=%s)", len(chunks)
        )
        return f"{system_prompt}\n\n{block}"


class AwarenessGateInterceptor:
    """PRE: strip spoiler phrases below awareness threshold."""

    priority = 40
    name = "AwarenessGateInterceptor"

    def gate(self, text: str, awareness: float) -> str:
        """
        Replace spoiler terms when awareness is below threshold.

        Args:
            text: Prompt or narration text.
            awareness: Player awareness 0–100.

        Returns:
            Gated text.
        """
        threshold = float(get_config().get("awareness.spoiler_gate_threshold", 15))
        if awareness >= threshold:
            return text

        result = text
        for pattern, replacement in _SPOILER_TERMS:
            result = pattern.sub(replacement, result)
        return result

    def run_pre(self, state: GameState, system_prompt: str, **_: Any) -> str:
        return self.gate(system_prompt, state.awareness)


def run_pre_interceptors(
    state: GameState,
    system_prompt: str,
    *,
    player_action: str = "",
    interceptors: Optional[list[Any]] = None,
) -> str:
    """
    Run configured PRE interceptors in priority order.

    Args:
        state: Current game state.
        system_prompt: Storyteller system prompt.
        player_action: Current player action for lore query.
        interceptors: Optional override list (tests).

    Returns:
        Modified system prompt.
    """
    cfg_names = get_config().get("comms.interceptors", []) or []
    if interceptors is None:
        registry = {
            "LoreInjectInterceptor": LoreInjectInterceptor(),
            "AwarenessGateInterceptor": AwarenessGateInterceptor(),
        }
        chain = [registry[n] for n in cfg_names if n in registry]
        if not chain:
            chain = [
                LoreInjectInterceptor(),
                AwarenessGateInterceptor(),
            ]
    else:
        chain = sorted(interceptors, key=lambda i: getattr(i, "priority", 99))

    result = system_prompt
    for interceptor in chain:
        run = getattr(interceptor, "run_pre", None)
        if callable(run):
            result = run(state, result, player_action=player_action)
    return result