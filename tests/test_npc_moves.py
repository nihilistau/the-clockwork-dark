"""
NPCs move with the Dark
=======================

As Doom Clock beats fire, named villagers abandon their posts and pull into the
square; ``npcs_at`` reflects it. See engine/game/world_effects.py,
data/world/doom_effects.yaml, [[the-village-empties]].
"""

from __future__ import annotations

import pytest

from engine.game.procgen import new_game_state
from engine.game.state import GameState
from engine.game.world_effects import apply_beat_effects, reset_doom_effects_cache


@pytest.fixture(autouse=True)
def _fresh():
    reset_doom_effects_cache()
    yield
    reset_doom_effects_cache()


def _ids_at(state, loc):
    return {n["id"] for n in state.procgen.npcs_at(loc)}


def test_vines_breach_drives_aldric_into_the_square():
    s = new_game_state(seed=4)
    assert s.procgen.npc_by_id("npc_aldric")["location_id"] == "forest_forage"
    assert "npc_aldric" not in _ids_at(s, "edgewood_square")

    applied = apply_beat_effects(s, "vines_breach_forest")

    aldric = s.procgen.npc_by_id("npc_aldric")
    assert aldric["location_id"] == "edgewood_square"
    assert aldric.get("displaced") is True
    assert "npc_aldric" in _ids_at(s, "edgewood_square")
    assert "npc_aldric" not in _ids_at(s, "forest_forage")
    assert {"type": "npc_move", "value": "npc_aldric->edgewood_square"} in applied


def test_tunnels_open_empties_the_shrine():
    s = new_game_state(seed=4)
    assert s.procgen.npc_by_id("npc_greta")["location_id"] == "edgewood_shrine"
    apply_beat_effects(s, "tunnels_open")
    assert s.procgen.npc_by_id("npc_greta")["location_id"] == "edgewood_square"
    assert "npc_greta" not in _ids_at(s, "edgewood_shrine")


def test_maris_does_not_move():
    s = new_game_state(seed=4)
    for beat in ("harvest_south", "scarecrow_wakes", "vines_breach_forest",
                 "tunnels_open", "tower_assembles"):
        apply_beat_effects(s, beat)
    assert s.procgen.npc_by_id("npc_maris")["location_id"] == "edgewood_bakery"


def test_npc_move_is_idempotent():
    s = new_game_state(seed=4)
    apply_beat_effects(s, "vines_breach_forest")
    count = len(s.procgen.npcs)
    again = apply_beat_effects(s, "vines_breach_forest")
    assert len(s.procgen.npcs) == count  # no duplicate npc
    assert not any(a["type"] == "npc_move" for a in again)


def test_unknown_npc_is_created_when_moved():
    s = GameState()  # empty procgen roster
    apply_beat_effects(s, "tunnels_open")  # moves npc_greta, absent here
    greta = s.procgen.npc_by_id("npc_greta")
    assert greta is not None
    assert greta["location_id"] == "edgewood_square"
