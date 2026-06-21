"""Chance encounters on travel — deterministic (seeded rng) tests (PR-more-world)."""

from __future__ import annotations

import random

from engine.game.encounters import (
    KIND_AMBUSH,
    KIND_DISCOVERY,
    KIND_NONE,
    Encounter,
    grant_discovery,
    reset_encounter_cache,
    roll_encounter,
)
from engine.game.combat import load_bestiary, reset_bestiary_cache
from engine.game.engine import GameEngine, set_active_engine
from engine.game.state import EvilPhase, GameState
from engine.skills.registry import SKILL_REGISTRY
import engine.skills.builtin.mechanics  # noqa: F401  (registers skills)
import json


def setup_function() -> None:
    reset_encounter_cache()
    reset_bestiary_cache()


def teardown_function() -> None:
    reset_encounter_cache()
    reset_bestiary_cache()


# --- calm-by-default --------------------------------------------------------

def test_no_danger_is_always_calm():
    # danger_dc below the floor (town hops / interiors) -> never an encounter.
    for dc in (0, 1, 7):
        enc = roll_encounter(dc, "consuming", rng=random.Random(1))
        assert enc.kind == KIND_NONE


def test_deterministic_for_same_seed():
    a = roll_encounter(16, "spreading", rng=random.Random(42))
    b = roll_encounter(16, "spreading", rng=random.Random(42))
    assert a.to_dict() == b.to_dict()


def test_dormant_travel_is_usually_calm():
    # Over many seeds at a moderate danger, dormant travel is calm the large majority
    # of the time — the quiet life is the default.
    rng = random.Random(7)
    kinds = [roll_encounter(10, "dormant", rng=rng).kind for _ in range(400)]
    calm = kinds.count(KIND_NONE)
    assert calm / len(kinds) > 0.85


# --- the roll scales with danger and phase ---------------------------------

def test_ambushes_appear_and_name_clockwork_foes():
    bestiary = load_bestiary()
    rng = random.Random(3)
    ambushes = [
        e for e in (roll_encounter(18, "consuming", rng=rng) for _ in range(500))
        if e.kind == KIND_AMBUSH
    ]
    assert ambushes, "high danger + consuming phase should yield some ambushes"
    for e in ambushes:
        assert e.enemy_id in bestiary
        assert "clockwork" in bestiary[e.enemy_id].get("tags", [])


def test_higher_phase_yields_more_encounters():
    def fired(phase: str) -> int:
        rng = random.Random(99)
        return sum(
            1 for _ in range(500)
            if roll_encounter(16, phase, rng=rng).kind != KIND_NONE
        )

    assert fired("consuming") > fired("dormant")


def test_discovery_carries_a_reward_item():
    rng = random.Random(5)
    disc = next(
        e for e in (roll_encounter(14, "stirring", rng=rng) for _ in range(500))
        if e.kind == KIND_DISCOVERY
    )
    assert disc.reward.get("item", {}).get("id")


# --- granting a discovery is engine-authoritative --------------------------

def test_grant_discovery_adds_item():
    state = GameState()
    enc = Encounter(kind=KIND_DISCOVERY, reward={"item": {"id": "wild_herbs", "name": "Wild Herbs"}})
    applied = grant_discovery(state, enc)
    assert applied.get("item", {}).get("id") == "wild_herbs"
    assert any(i.id == "wild_herbs" for i in state.inventory)


def test_grant_discovery_noop_for_ambush():
    state = GameState()
    enc = Encounter(kind=KIND_AMBUSH, enemy_id="clockwork_beast")
    assert grant_discovery(state, enc) == {}
    assert state.inventory == []


# --- move_to hook: backward compatible -------------------------------------

def test_move_to_attaches_encounter_field_only_when_present():
    # A zero-danger town hop never produces an encounter -> field stays None and is
    # omitted from to_dict (existing callers unaffected).
    state = GameState(location_id="edgewood_square")
    state.stats.stamina = 100
    res = GameEngine(state).move_to("edgewood_bakery")
    assert res.success is True
    assert res.encounter is None
    assert "encounter" not in res.to_dict()


def test_move_to_hook_can_fire_with_seeded_rng():
    # Drive the private hook directly with a max-ish rng to force an encounter on a
    # dangerous edge, proving the hook computes + (for discovery) grants.
    state = GameState(location_id="forest_clearing", evil_phase=EvilPhase.CONSUMING)
    state.evil_progress = 0.85
    engine = GameEngine(state)
    # A consuming-phase, high-danger edge: chance caps at 0.6. Seed 1's first
    # random() is ~0.134 (< 0.6) -> an encounter fires, deterministically.
    enc = engine._roll_arrival_encounter({"danger_dc": 18}, rng=random.Random(1))
    assert enc is not None
    assert enc["kind"] in (KIND_AMBUSH, KIND_DISCOVERY)


def test_move_to_skill_still_succeeds_and_moves():
    # The registered move_to skill must keep working exactly as before.
    state = GameState(location_id="forest_clearing")
    state.stats.stamina = 100
    set_active_engine(GameEngine(state))
    raw = SKILL_REGISTRY.invoke("move_to", location_id="edgewood_square")
    data = json.loads(raw)
    assert data["success"] is True
    assert state.location_id == "edgewood_square"


# --- the read-only foe-listing skill ---------------------------------------

def test_query_encounter_foes_skill():
    state = GameState(evil_phase=EvilPhase.SPREADING)
    set_active_engine(GameEngine(state))
    raw = SKILL_REGISTRY.invoke("query_encounter_foes")
    data = json.loads(raw)
    assert data["evil_phase"] == "spreading"
    assert data["foes"]
    bestiary = load_bestiary()
    for foe in data["foes"]:
        assert "clockwork" in bestiary[foe["id"]].get("tags", [])
