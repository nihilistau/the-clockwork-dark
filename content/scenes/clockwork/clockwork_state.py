"""
Clockwork Session State
=======================

In-memory session store for active games.

Version: v0.1.0 [2026-06-20]
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Optional

from engine.agents.assistant import AssistantAgent
from engine.agents.storyteller import StorytellerAgent
from engine.design.assets import place_metadata, resolve_location_image
from engine.game.engine import GameEngine, set_active_engine
from engine.game.procgen import new_game_state
from engine.world.content import (
    location_metadata,
    mural_fragment_for_phase,
    overlay_for_location,
    rumors_for_phase,
)
from engine.world.world_sim import WorldSim, merge_npcs_at_location

logger = logging.getLogger(__name__)

OPENING_NARRATION = (
    "You wake beneath birch trees at the forest's edge. "
    "Mist clings to the ferns; somewhere ahead, hearth smoke threads the grey."
)
OPENING_CHOICES = [
    {"id": "a", "text": "Follow the smoke toward Edgewood"},
    {"id": "b", "text": "Search the clearing for supplies"},
    {"id": "c", "text": "Listen — something watches without moving"},
]


@dataclass
class GameSession:
    """One player session bound to engine and agents."""

    engine: GameEngine
    storyteller: StorytellerAgent
    assistant: AssistantAgent
    last_turn: dict[str, Any] = field(default_factory=dict)

    @property
    def session_id(self) -> str:
        return self.engine.state.session_id


class SessionStore:
    """Thread-safe enough in-memory session registry for v0.1."""

    def __init__(self) -> None:
        self._sessions: dict[str, GameSession] = {}

    def create(
        self,
        *,
        player_name: str = "Traveler",
        archetype: str = "wayfarer",
        seed: Optional[int] = None,
        llm_fn: Optional[Callable[[list[dict[str, Any]]], str]] = None,
    ) -> GameSession:
        """Create a new procgen-backed session."""
        state = new_game_state(
            player_name=player_name,
            archetype=archetype,
            seed=seed,
        )
        engine = GameEngine(state)
        set_active_engine(engine)
        opening_place = place_metadata(state.location_id)
        opening_image = resolve_location_image(state.location_id) or ""
        opening_meta = location_metadata(state.location_id)
        session = GameSession(
            engine=engine,
            storyteller=StorytellerAgent(engine, llm_fn=llm_fn),
            assistant=AssistantAgent(engine, llm_fn=llm_fn),
            last_turn={
                "narration": OPENING_NARRATION,
                "choices": OPENING_CHOICES,
                "state": state.to_dict(),
                "scene": _scene_payload(state, opening_place, opening_image, opening_meta),
            },
        )
        self._sessions[state.session_id] = session
        logger.info(
            "[clockwork_state] Session created (operation=create, id=%s)",
            state.session_id,
        )
        return session

    def get(self, session_id: str) -> Optional[GameSession]:
        return self._sessions.get(session_id)

    def require(self, session_id: str) -> GameSession:
        session = self.get(session_id)
        if session is None:
            raise KeyError(f"Unknown session: {session_id}")
        return session

    def delete(self, session_id: str) -> None:
        self._sessions.pop(session_id, None)


def _scene_payload(
    state: Any,
    place: dict[str, Any],
    image_url: str,
    meta: dict[str, Any],
) -> dict[str, Any]:
    """Build scene block for turn payloads."""
    from engine.game.combat import combat_snapshot

    in_combat = state.combat is not None
    return {
        "location_id": state.location_id,
        "name": place.get("name", state.location_id),
        "caption": place.get("caption", ""),
        "image_url": image_url,
        "kind": meta.get("kind", place.get("kind", "")),
        "combat": combat_snapshot(state) if in_combat else None,
        "overlay": "combat" if in_combat else (meta.get("overlay") or overlay_for_location(state.location_id)),
        "cutscene_id": meta.get("cutscene_id", ""),
        "npcs": merge_npcs_at_location(state, state.location_id),
        "mural_fragment": mural_fragment_for_phase(state.evil_phase.value),
        "rumors": rumors_for_phase(state.evil_phase.value)[:3],
    }


def resolve_player_action(
    session: GameSession,
    choice_id: str,
    custom_text: Optional[str] = None,
) -> str:
    """Map choice id or custom text to Storyteller user message."""
    if custom_text and custom_text.strip():
        return custom_text.strip()

    choices = session.last_turn.get("choices", [])
    for choice in choices:
        if choice.get("id") == choice_id:
            return f"The player chooses: {choice.get('text', choice_id)}"
    return f"The player chooses option {choice_id}"


def run_turn(
    session: GameSession,
    player_action: str,
    *,
    emit_callback: Optional[Callable[[str, dict[str, Any]], None]] = None,
) -> dict[str, Any]:
    """
    Execute Storyteller + Assistant turn and build turn_update payload.

    Args:
        session: Active game session.
        player_action: Resolved player action text.
        emit_callback: Optional (event_name, payload) emitter for Socket.IO.

    Returns:
        turn_update dict.
    """
    set_active_engine(session.engine)
    state = session.engine.state

    if WorldSim.should_run_realtime_tick(state.last_sim_tick_at):
        WorldSim.on_tick(state, days_elapsed=0.25)

    # Stream narration prose to the client live (epilogue withheld by the gate).
    on_delta = None
    if emit_callback is not None:
        on_delta = lambda chunk: emit_callback("narration_delta", chunk)  # noqa: E731

    _t0 = time.perf_counter()
    storyteller_result = session.storyteller.run_turn(player_action, on_delta=on_delta)
    assistant_result = session.assistant.run_turn(storyteller_result.narration)

    # Fire a story-milestone cutscene if one is due (phase-shift budgeted).
    from engine.media.milestones import CutsceneMilestones

    milestone_job = CutsceneMilestones.trigger(state)
    if milestone_job is not None:
        storyteller_result.media.setdefault("cutscenes", []).append(
            {"url": milestone_job.url, "payload": milestone_job.payload}
        )

    scene_meta = place_metadata(state.location_id)
    loc_meta = location_metadata(state.location_id)
    scene_image = scene_meta.get("image_url", "") or resolve_location_image(state.location_id) or ""
    turn_payload = {
        "session_id": state.session_id,
        "narration": storyteller_result.narration,
        "choices": storyteller_result.choices,
        "state": state.to_dict(),
        "tool_receipts": storyteller_result.tool_receipts,
        "evaluation": storyteller_result.evaluation.to_dict(),
        "media": storyteller_result.media,
        "governance": storyteller_result.governance,
        "assistant": assistant_result.to_dict(),
        "scene": _scene_payload(state, scene_meta, scene_image, loc_meta),
    }
    session.last_turn = turn_payload

    # Telemetry: roll this turn into the Oracle metrics.
    from engine.observability import get_oracle

    get_oracle().record_turn(
        turn_payload,
        latency_ms=(time.perf_counter() - _t0) * 1000.0,
        evil_progress=state.evil_progress,
    )

    if emit_callback:
        emit_callback("turn_update", turn_payload)
        for receipt in storyteller_result.tool_receipts:
            if receipt.get("type") == "dice":
                dice_payload = dict(receipt.get("result", {}))
                dice_data = dice_payload.get("dice", dice_payload)
                emit_callback("dice_result", dice_data)
        if assistant_result.spoke:
            emit_callback(
                "assistant_speak",
                {
                    "text": assistant_result.text,
                    "form": assistant_result.form,
                    "voice_style": assistant_result.voice_style,
                },
            )
        for img in storyteller_result.media.get("images", []):
            emit_callback(
                "image_ready",
                {
                    "url": img.get("url", ""),
                    "location_id": img.get("payload", {}).get("location_id", ""),
                },
            )
        for cut in storyteller_result.media.get("cutscenes", []):
            emit_callback(
                "cutscene_start",
                {
                    "id": cut.get("payload", {}).get("cutscene_id", ""),
                    "video_url": cut.get("url", ""),
                    "captions": cut.get("payload", {}).get("captions", []),
                },
            )

    return turn_payload