"""
WorldSim
========

Background world ticks — evil advance, schedules, plot pressure.

Version: v0.1.0 [2026-06-20]
"""

from __future__ import annotations

import logging
import random
import time
from typing import Any, Optional

from engine.config import get_config
from engine.game.evil_ticker import EvilTicker
from engine.game.plot import PlotFormula
from engine.game.state import GameState
from engine.world.schedules import ScheduleRoll, SimEvent, load_schedules

logger = logging.getLogger(__name__)


def visiting_npcs_at_location(state: GameState, location_id: str) -> list[dict[str, Any]]:
    """
    Return NPC presence entries from active world events at a location.

    Args:
        state: Current game state.
        location_id: Location to query.

    Returns:
        List of dicts with id, name, role, visiting=True.
    """
    present: list[dict[str, Any]] = []
    seen: set[str] = set()
    for raw in state.world_events:
        if raw.get("location_id") != location_id:
            continue
        for npc_id in raw.get("npc_ids", []):
            if npc_id in seen:
                continue
            seen.add(npc_id)
            procgen_npc = state.procgen.npc_by_id(str(npc_id))
            if procgen_npc:
                entry = dict(procgen_npc)
            else:
                entry = {"id": npc_id, "name": npc_id, "role": "visitor"}
            entry["visiting"] = True
            entry["event_id"] = raw.get("event_id")
            present.append(entry)
    return present


def _event_npc_map(state: GameState, location_id: str) -> dict[str, str]:
    """Map npc_id -> event_id for active events at location."""
    mapping: dict[str, str] = {}
    for raw in state.world_events:
        if raw.get("location_id") != location_id:
            continue
        event_id = str(raw.get("event_id", ""))
        for npc_id in raw.get("npc_ids", []):
            mapping[str(npc_id)] = event_id
    return mapping


def merge_npcs_at_location(state: GameState, location_id: str) -> list[dict[str, Any]]:
    """Merge procgen NPCs with visiting event NPCs."""
    event_npcs = _event_npc_map(state, location_id)
    base = [dict(n) for n in state.procgen.npcs_at(location_id)]
    base_ids = {n.get("id") for n in base}
    for entry in base:
        npc_id = entry.get("id")
        if npc_id in event_npcs:
            entry["visiting"] = True
            entry["event_id"] = event_npcs[npc_id]
    for visitor in visiting_npcs_at_location(state, location_id):
        if visitor.get("id") not in base_ids:
            base.append(visitor)
    return base


class WorldSim:
    """Orchestrates world tick side effects."""

    @staticmethod
    def tick_interval_seconds() -> int:
        """Real-time seconds between optional background ticks."""
        return int(get_config().get("world.tick_interval_seconds", 60))

    @staticmethod
    def should_run_realtime_tick(
        last_tick_at: float,
        *,
        now: Optional[float] = None,
    ) -> bool:
        """Return True if real-time interval elapsed since last_tick_at."""
        if last_tick_at <= 0:
            return True
        current = now if now is not None else time.time()
        return (current - last_tick_at) >= WorldSim.tick_interval_seconds()

    @staticmethod
    def _rng_for_state(state: GameState) -> random.Random:
        return random.Random(state.procgen.seed + state.world_day * 9973)

    @staticmethod
    def expire_events(state: GameState) -> None:
        """Remove world events past expires_day."""
        state.world_events = [
            e
            for e in state.world_events
            if int(e.get("expires_day", state.world_day)) >= state.world_day
        ]

    @staticmethod
    def apply_events(state: GameState, events: list[SimEvent]) -> None:
        """Persist events and rumors on state."""
        for event in events:
            state.world_events = [
                e for e in state.world_events if e.get("event_id") != event.event_id
            ]
            state.world_events.append(event.to_dict())
            rumor = event.payload.get("rumor")
            if rumor and rumor not in state.rumors:
                state.rumors.append(str(rumor))
            logger.info(
                "[world_sim] Event applied (operation=apply_events, event=%s, day=%s)",
                event.event_id,
                event.day,
            )

    @staticmethod
    def on_tick(
        state: GameState,
        *,
        days_elapsed: float = 1.0,
        rng: Optional[random.Random] = None,
        force: Optional[list[str]] = None,
    ) -> list[SimEvent]:
        """
        Advance world simulation for elapsed in-game days.

        Args:
            state: Mutable game state.
            days_elapsed: In-game days to advance.
            rng: Optional RNG override for tests.
            force: Force specific event ids (caravan_arrival, tinker_camp, militia_press).

        Returns:
            List of SimEvent emitted this tick.
        """
        force_set = set(force or [])
        roll_rng = rng or WorldSim._rng_for_state(state)
        schedules = load_schedules()

        state.world_day += int(days_elapsed)
        state.last_sim_tick_at = time.time()
        EvilTicker.advance(state, days_elapsed=days_elapsed)
        PlotFormula.update_story_pressure(state)
        WorldSim.expire_events(state)

        events: list[SimEvent] = []
        events.extend(
            ScheduleRoll.check_caravan(
                state,
                roll_rng,
                schedules=schedules,
                force="caravan_arrival" in force_set,
            )
        )
        events.extend(
            ScheduleRoll.check_tinker(
                state,
                roll_rng,
                days_elapsed=days_elapsed,
                schedules=schedules,
                force="tinker_camp" in force_set,
            )
        )
        events.extend(
            ScheduleRoll.check_militia(
                state,
                roll_rng,
                schedules=schedules,
                force="militia_press" in force_set,
            )
        )

        WorldSim.apply_events(state, events)
        return events