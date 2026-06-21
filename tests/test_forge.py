"""
The Forge — a new location + crafting station
=============================================

Brann Holt's smithy off the square: reachable, canonical, and a station-gated
crafting bench for arms and anti-Dark wards. See data/world/content.yaml,
data/recipes/forge.yaml, [[the-forge]].
"""

from __future__ import annotations

import pytest

from engine.game.crafting import craft_item, reset_recipe_cache
from engine.game.engine import GameEngine
from engine.game.locations import get_location, reload_locations
from engine.game.procgen import new_game_state
from engine.game.state import GameState, InventoryItem


class _MaxRng:
    """Force a natural 20 so the craft check always succeeds."""

    def randint(self, _a: int, _b: int) -> int:
        return 20


@pytest.fixture(autouse=True)
def _fresh():
    reset_recipe_cache()
    reload_locations()
    yield
    reset_recipe_cache()
    reload_locations()


def test_forge_is_a_canonical_location_off_the_square():
    reload_locations()
    assert get_location("edgewood_forge") is not None
    s = new_game_state(seed=2)
    s.location_id = "edgewood_square"
    eng = GameEngine(s)
    res = eng.move_to("edgewood_forge")
    assert res.success is True
    assert s.location_id == "edgewood_forge"


def test_brann_keeps_the_forge():
    s = new_game_state(seed=2)
    assert s.procgen.npc_by_id("npc_brann")["location_id"] == "edgewood_forge"
    assert "npc_brann" in {n["id"] for n in s.procgen.npcs_at("edgewood_forge")}


def _stocked(loc: str) -> GameState:
    s = GameState()
    s.location_id = loc
    s.inventory.append(InventoryItem(id="brass_filings", name="Brass Filings", qty=3))
    s.inventory.append(InventoryItem(id="sympathy_charm", name="Sympathy Charm", qty=1))
    return s


def test_warded_blade_forged_at_the_anvil():
    s = _stocked("edgewood_forge")
    res = craft_item(s, "forge_warded_blade", rng=_MaxRng())
    assert res.outcome == "crafted", res.message
    assert any(i.id == "warded_blade" for i in s.inventory)


def test_warded_blade_cannot_be_forged_off_station():
    s = _stocked("edgewood_square")  # right inputs, wrong place
    res = craft_item(s, "forge_warded_blade", rng=_MaxRng())
    assert res.outcome == "wrong_station"
    assert not any(i.id == "warded_blade" for i in s.inventory)
