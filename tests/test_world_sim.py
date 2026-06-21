"""WorldSim and trader schedule tests."""

from __future__ import annotations

import json

import engine.skills.builtin.mechanics  # noqa: F401 — register skills
from engine.game.engine import GameEngine, set_active_engine
from engine.game.procgen import new_game_state
from engine.skills.registry import SKILL_REGISTRY
from engine.world.schedules import ScheduleRoll, load_schedules
from engine.world.world_sim import WorldSim, merge_npcs_at_location, visiting_npcs_at_location


def _engine(day: int = 6, *, awareness: float = 0.0, seed: int = 42) -> GameEngine:
    state = new_game_state(seed=seed)
    state.world_day = day
    state.awareness = awareness
    return GameEngine(state)


def test_schedules_load():
    schedules = load_schedules()
    assert "caravan_arrival" in schedules
    assert len(schedules.get("rumors", [])) >= 3


def test_caravan_blocked_before_day_5():
    engine = _engine(day=4)
    events = WorldSim.on_tick(
        engine.state,
        days_elapsed=0,
        force=["caravan_arrival"],
    )
    assert events == []


def test_caravan_forced_tick():
    engine = _engine(day=6)
    result = engine.advance_world_day(days=1, force_events=["caravan_arrival"])
    assert len(result["events"]) == 1
    assert result["events"][0]["event_id"] == "caravan_arrival"
    assert result["events"][0]["npc_ids"] == ["npc_odran"]
    assert len(result["rumors"]) == 1
    assert engine.state.world_events[0]["event_id"] == "caravan_arrival"


def test_tinker_forced_tick():
    engine = _engine(day=10)
    events = WorldSim.on_tick(engine.state, days_elapsed=1, force=["tinker_camp"])
    assert len(events) == 1
    assert events[0].event_id == "tinker_camp"
    assert events[0].location_id == "tinker_caravan"


def test_militia_requires_awareness():
    engine = _engine(day=10, awareness=10.0)
    events = WorldSim.on_tick(engine.state, force=["militia_press"])
    assert events == []

    engine.state.awareness = 25.0
    events = WorldSim.on_tick(engine.state, force=["militia_press"])
    assert len(events) == 1
    assert events[0].event_id == "militia_press"


def test_on_tick_advances_evil():
    engine = _engine(day=6)
    before = engine.state.evil_progress
    WorldSim.on_tick(engine.state, days_elapsed=2)
    assert engine.state.world_day == 8
    assert engine.state.evil_progress > before


def test_visiting_npc_merge():
    engine = _engine(day=6)
    engine.advance_world_day(days=1, force_events=["caravan_arrival"])
    visitors = visiting_npcs_at_location(engine.state, "edgewood_square")
    assert any(v["id"] == "npc_odran" for v in visitors)
    merged = merge_npcs_at_location(engine.state, "edgewood_square")
    odran_entries = [n for n in merged if n.get("id") == "npc_odran"]
    assert len(odran_entries) == 1
    assert odran_entries[0].get("visiting") is True


def test_advance_world_tick_skill_force():
    engine = _engine(day=7)
    set_active_engine(engine)
    raw = SKILL_REGISTRY.invoke(
        "advance_world_tick",
        days=1.0,
        force_event="caravan_arrival",
    )
    data = json.loads(raw)
    assert data["events"][0]["event_id"] == "caravan_arrival"
    assert data["rumors"]


def test_events_expire():
    engine = _engine(day=6)
    WorldSim.on_tick(engine.state, days_elapsed=1, force=["caravan_arrival"])
    assert engine.state.world_events
    engine.state.world_day = 20
    WorldSim.expire_events(engine.state)
    assert engine.state.world_events == []


def test_realtime_tick_interval():
    assert WorldSim.should_run_realtime_tick(0.0, now=100.0) is True
    assert WorldSim.should_run_realtime_tick(100.0, now=120.0) is False
    assert WorldSim.should_run_realtime_tick(100.0, now=200.0) is True


def test_schedule_roll_no_duplicate_caravan():
    engine = _engine(day=6)
    WorldSim.on_tick(engine.state, force=["caravan_arrival"])
    second = ScheduleRoll.check_caravan(engine.state, WorldSim._rng_for_state(engine.state), force=True)
    assert second == []