"""Crafting tests (PR14, v0.2)."""

from __future__ import annotations

import json
import random

import pytest

from engine.game.crafting import (
    craft_item,
    list_recipes,
    load_recipes,
    reset_recipe_cache,
)
from engine.game.engine import GameEngine, set_active_engine
from engine.game.state import GameState, InventoryItem
from engine.skills.registry import SKILL_REGISTRY
import engine.skills.builtin.mechanics  # noqa: F401


class _MaxRng(random.Random):
    def randint(self, a: int, b: int) -> int:  # type: ignore[override]
        return b


class _MinRng(random.Random):
    def randint(self, a: int, b: int) -> int:  # type: ignore[override]
        return a


@pytest.fixture(autouse=True)
def _reset():
    reset_recipe_cache()
    yield
    reset_recipe_cache()


def _give(state: GameState, item_id: str, qty: int, name: str = "") -> None:
    state.inventory.append(InventoryItem(id=item_id, name=name or item_id, qty=qty))


def _qty(state: GameState, item_id: str) -> int:
    item = next((i for i in state.inventory if i.id == item_id), None)
    return item.qty if item else 0


def test_recipes_load():
    recipes = load_recipes()
    for rid in ("herb_poultice", "forest_tonic", "hearth_loaf", "warding_charm"):
        assert rid in recipes
        assert recipes[rid]["output"]["id"]


def test_unknown_recipe():
    state = GameState()
    res = craft_item(state, "moon_cheese")
    assert res.outcome == "unknown"
    assert not res.success


def test_craft_success_consumes_inputs_and_grants_output():
    state = GameState()
    _give(state, "wild_herbs", 2)
    res = craft_item(state, "herb_poultice", rng=_MaxRng())
    assert res.success
    assert res.outcome == "crafted"
    assert _qty(state, "wild_herbs") == 0          # consumed 2
    assert _qty(state, "bandage_poultice") >= 1    # output granted
    assert state.stats.craft == 11                 # practice +1


def test_missing_inputs_blocks_craft():
    state = GameState()
    _give(state, "wild_herbs", 1)  # need 2
    res = craft_item(state, "herb_poultice", rng=_MaxRng())
    assert res.outcome == "missing_inputs"
    assert _qty(state, "wild_herbs") == 1  # not consumed


def test_wrong_station_blocks_craft():
    state = GameState()  # starts at forest_clearing
    _give(state, "honeycomb", 1)
    _give(state, "wild_berry", 1)
    res = craft_item(state, "hearth_loaf", rng=_MaxRng())  # needs edgewood_bakery
    assert res.outcome == "wrong_station"
    assert _qty(state, "honeycomb") == 1


def test_station_match_allows_craft():
    state = GameState()
    state.location_id = "edgewood_bakery"
    _give(state, "honeycomb", 1)
    _give(state, "wild_berry", 1)
    res = craft_item(state, "hearth_loaf", rng=_MaxRng())
    assert res.success
    assert _qty(state, "loaf") >= 1


def test_crit_yields_fine_extra():
    state = GameState()
    _give(state, "wild_herbs", 2)
    res = craft_item(state, "herb_poultice", rng=_MaxRng())  # nat 20 -> crit
    assert res.quality == "fine"
    assert res.output["qty"] == 2  # base 1 + fine extra


def test_focus_recipe_requires_and_spends_focus():
    state = GameState()
    state.location_id = "tinker_caravan"
    _give(state, "brass_filings", 1)
    _give(state, "old_clock_part", 1)
    state.stats.focus = 1  # warding_charm needs focus_cost 2
    res = craft_item(state, "warding_charm", rng=_MaxRng())
    assert res.outcome == "no_focus"
    assert _qty(state, "brass_filings") == 1  # not consumed


def test_ordinary_miss_keeps_materials():
    state = GameState()
    _give(state, "wild_herbs", 2)
    # roll a 2 (no fumble, below dc 9) -> failed, materials intact
    class _TwoRng(random.Random):
        def randint(self, a, b):
            return 2 if b == 20 else a
    res = craft_item(state, "herb_poultice", rng=_TwoRng())
    assert res.outcome == "failed"
    assert _qty(state, "wild_herbs") == 2


def test_fumble_spoils_materials():
    state = GameState()
    _give(state, "wild_herbs", 2)
    res = craft_item(state, "herb_poultice", rng=_MinRng())  # nat 1 -> fumble
    assert res.outcome == "spoiled"
    assert _qty(state, "wild_herbs") == 0  # ruined


def test_list_recipes_flags_craftable():
    state = GameState()
    _give(state, "wild_herbs", 2)
    listed = {r["id"]: r for r in list_recipes(state)}
    assert listed["herb_poultice"]["can_craft"] is True
    assert listed["warding_charm"]["can_craft"] is False  # no inputs/station


def test_craft_via_registry():
    state = GameState()
    _give(state, "wild_herbs", 2)
    engine = GameEngine(state)
    set_active_engine(engine)
    payload = json.loads(SKILL_REGISTRY.invoke("craft_item", recipe_id="herb_poultice"))
    assert payload["recipe_id"] == "herb_poultice"
    assert "outcome" in payload
    listing = json.loads(SKILL_REGISTRY.invoke("list_recipes"))
    assert any(r["id"] == "forest_tonic" for r in listing)
