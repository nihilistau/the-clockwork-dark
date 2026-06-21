"""Grounded combat tests (PR13, v0.2)."""

from __future__ import annotations

import json
import random

import pytest

from engine.game.combat import (
    CombatResult,
    load_bestiary,
    reset_bestiary_cache,
    resolve_combat,
    start_combat,
)
from engine.game.engine import GameEngine, set_active_engine
from engine.game.state import GameState, InventoryItem
from engine.skills.registry import SKILL_REGISTRY
import engine.skills.builtin.mechanics  # noqa: F401  (registers skills)


class _MaxRng(random.Random):
    """Always rolls the top face — forces crits/hits and max damage."""

    def randint(self, a: int, b: int) -> int:  # type: ignore[override]
        return b


class _MinRng(random.Random):
    """Always rolls 1 — forces fumbles/misses."""

    def randint(self, a: int, b: int) -> int:  # type: ignore[override]
        return a


@pytest.fixture(autouse=True)
def _reset():
    reset_bestiary_cache()
    yield
    reset_bestiary_cache()


def _fresh_state() -> GameState:
    return GameState()


def test_bestiary_loads_canon_enemies():
    bestiary = load_bestiary()
    for eid in ("wolf", "scarecrow_brass", "clockwork_beast", "husk", "deserter"):
        assert eid in bestiary
        assert bestiary[eid]["hp"] > 0


def test_start_combat_sets_encounter():
    state = _fresh_state()
    res = start_combat(state, "wolf")
    assert res.success
    assert state.combat is not None
    assert state.combat["enemy_id"] == "wolf"
    assert state.combat["enemy_hp"] == state.combat["enemy_max_hp"] == 9


def test_unknown_enemy_errors():
    state = _fresh_state()
    res = start_combat(state, "grue")
    assert res.outcome == "error"
    assert state.combat is None


def test_resolve_without_combat_or_target_errors():
    state = _fresh_state()
    res = resolve_combat(state, "attack")
    assert res.outcome == "error"


def test_attack_crit_kills_weak_foe_is_victory():
    state = _fresh_state()
    res = resolve_combat(state, "attack", target_id="wolf", rng=_MaxRng())
    assert res.victory is True
    assert res.ended is True
    assert res.damage_dealt >= 9
    assert state.combat is None  # encounter cleared on victory


def test_attack_invariants_with_seeded_rng():
    state = _fresh_state()
    start_combat(state, "clockwork_beast")
    before = state.combat["enemy_hp"]
    res = resolve_combat(state, "attack", rng=random.Random(7))
    assert res.round == 1
    # either we dealt damage (hit) or missed — never both
    if res.outcome == "hit":
        assert state.combat is None or state.combat["enemy_hp"] == before - res.damage_dealt
    else:
        assert res.outcome == "miss"
        assert res.damage_dealt == 0


def test_victory_grants_loot():
    state = _fresh_state()
    # clockwork_beast drops a Sympathy Charm
    while state.combat is None or not _is_over(state):
        res = resolve_combat(state, "attack", target_id="clockwork_beast", rng=_MaxRng())
        if res.ended:
            break
    assert res.victory is True
    assert any(i.id == "talisman" for i in state.inventory)


def _is_over(state: GameState) -> bool:
    return state.combat is None


def test_defeat_respawns_with_penalty():
    state = _fresh_state()
    state.stats.hp = 1
    start_combat(state, "wolf")
    res = resolve_combat(state, "defend", rng=_MaxRng())  # enemy crits through guard
    assert res.defeat is True
    assert res.ended is True
    assert state.location_id == "edgewood_square"
    assert state.stats.hp == state.stats.max_hp // 2
    assert state.flags.get("combat_defeat") is True
    assert state.combat is None


def test_flee_success_ends_combat():
    state = _fresh_state()
    start_combat(state, "wolf")
    res = resolve_combat(state, "flee", rng=_MaxRng())  # roll 20 >= flee_dc
    assert res.fled is True
    assert res.ended is True
    assert state.combat is None


def test_flee_failure_keeps_fighting():
    state = _fresh_state()
    start_combat(state, "wolf")
    res = resolve_combat(state, "flee", rng=_MinRng())  # roll 1 < flee_dc
    assert res.outcome == "flee_failed"
    assert res.ended is False
    assert state.combat is not None


def test_use_item_heals_and_consumes():
    state = _fresh_state()
    state.stats.hp = 5
    state.inventory.append(InventoryItem(id="bandage_poultice", name="Bandage Poultice", qty=1))
    start_combat(state, "wolf")
    res = resolve_combat(state, "use_item", item_id="bandage_poultice", rng=_MinRng())
    assert res.outcome == "item"
    assert state.stats.hp == 13  # 5 + 8, enemy missed (min rng)
    assert all(i.id != "bandage_poultice" for i in state.inventory)


def test_sympathy_unmakes_clockwork():
    state = _fresh_state()
    start_combat(state, "clockwork_beast")
    before = state.combat["enemy_hp"]
    res = resolve_combat(state, "sympathy", rng=_MaxRng())
    assert res.outcome == "sympathy_unmake"
    assert res.damage_dealt > 0
    assert res.focus == 10 - 3  # focus cost paid
    # enemy took unmaking damage (then countered, but hp tracked on enemy)
    assert res.enemy_hp == before - res.damage_dealt


def test_sympathy_requires_focus():
    state = _fresh_state()
    state.stats.focus = 1
    start_combat(state, "wolf")
    res = resolve_combat(state, "sympathy", rng=_MaxRng())
    assert res.outcome == "sympathy_failed"


def test_fear_and_exhaustion_apply_to_hit_penalty():
    state = _fresh_state()
    start_combat(state, "wolf")
    state.combat["fear"] = 9          # 9 // 3 = 3 penalty
    state.stats.stamina = 10          # below exhaustion threshold → +2
    res = resolve_combat(state, "attack", rng=random.Random(1))
    # modifier = player_attack_mod(2) - (3 + 2) = -3
    assert res.dice is not None
    assert res.dice["modifier"] == -3


def test_combat_persists_through_save_round_trip():
    state = _fresh_state()
    start_combat(state, "scarecrow_brass")
    data = state.to_dict(include_hidden=True)
    restored = GameState.from_dict(data)
    assert restored.combat is not None
    assert restored.combat["enemy_id"] == "scarecrow_brass"
    assert restored.combat["enemy_hp"] == state.combat["enemy_hp"]


def test_combat_skill_via_registry():
    state = _fresh_state()
    engine = GameEngine(state)
    set_active_engine(engine)
    raw = SKILL_REGISTRY.invoke("resolve_combat", action="attack", target_id="wolf")
    payload = json.loads(raw)
    assert payload["enemy_id"] == "wolf"
    assert "outcome" in payload
    snap = json.loads(SKILL_REGISTRY.invoke("query_combat_state"))
    # combat may have ended in one hit; snapshot reflects active flag either way
    assert "active" in snap
