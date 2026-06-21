"""
Reactive world tests
====================

Doom Clock beats mutate the world: flags, discoveries (the tunnels opening
unseals the hidden path), rumors, world_events, and flag-gated notice-board
postings. See engine/game/world_effects.py and [[the-reactive-world]].
"""

from __future__ import annotations

import pytest

from engine.game.contracts import ContractBoard, reset_contracts_cache
from engine.game.doom_clock import DoomClock
from engine.game.engine import GameEngine
from engine.game.procgen import new_game_state
from engine.game.state import GameState
from engine.game.world_effects import apply_beat_effects, reset_doom_effects_cache


@pytest.fixture(autouse=True)
def _fresh():
    reset_doom_effects_cache()
    reset_contracts_cache()
    yield
    reset_doom_effects_cache()
    reset_contracts_cache()


def test_apply_beat_effects_sets_flags_rumors_events():
    s = GameState()
    applied = apply_beat_effects(s, "scarecrow_wakes")
    assert s.flags.get("scarecrow_awake") is True
    assert any("scarecrow" in r.lower() for r in s.rumors)
    assert any(e.get("id") == "scarecrow_walks" for e in s.world_events)
    assert {"type": "flag", "value": "scarecrow_awake"} in applied


def test_apply_beat_effects_is_idempotent():
    s = GameState()
    apply_beat_effects(s, "tunnels_open")
    rumors1, events1 = list(s.rumors), list(s.world_events)
    second = apply_beat_effects(s, "tunnels_open")
    assert s.rumors == rumors1          # no duplicate rumors
    assert s.world_events == events1     # no duplicate events
    assert second == []                  # nothing newly applied


def test_unknown_beat_is_noop():
    s = GameState()
    assert apply_beat_effects(s, "no_such_beat") == []


def test_pending_beats_apply_world_effects():
    s = GameState()
    s.evil_progress = 0.7  # crosses harvest_south .. tunnels_open (not the tower)
    crossed = {b.id for b in DoomClock.pending_beats(s)}
    assert {"harvest_south", "scarecrow_wakes", "vines_breach_forest", "tunnels_open"} <= crossed
    assert s.flags.get("tunnels_open") is True
    assert s.flags.get("discovery_hidden_path") is True
    assert "tower_assembles" not in crossed


def test_tunnels_open_unseals_the_hidden_path():
    s = new_game_state(seed=5)
    s.location_id = "forest_clearing"
    eng = GameEngine(s)

    # Before: the barrow road is gated by the hidden_path discovery.
    assert eng.move_to("hollow_hill").success is False

    # The tunnels open (a Doom Clock beat) — the seam unseals the road.
    s.evil_progress = 0.7
    DoomClock.pending_beats(s)
    assert s.flags.get("discovery_hidden_path") is True

    s.location_id = "forest_clearing"
    opened = eng.move_to("hollow_hill")
    assert opened.success is True
    assert s.location_id == "hollow_hill"


def test_board_posts_seal_the_tunnel_only_after_beat():
    s = GameState()
    s.location_id = "edgewood_square"

    before = {c["id"] for c in ContractBoard.available(s)}
    assert "seal_the_tunnel" not in before

    apply_beat_effects(s, "tunnels_open")  # sets the tunnels_open flag
    after = {c["id"] for c in ContractBoard.available(s)}
    assert "seal_the_tunnel" in after

    accepted = ContractBoard.accept(s, "seal_the_tunnel")
    assert accepted["success"] is True


def test_flag_gated_contract_rejected_before_its_beat():
    s = GameState()
    s.location_id = "edgewood_square"
    res = ContractBoard.accept(s, "watch_the_walking_scarecrow")
    assert res["success"] is False
    apply_beat_effects(s, "scarecrow_wakes")
    assert ContractBoard.accept(s, "watch_the_walking_scarecrow")["success"] is True
