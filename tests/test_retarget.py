"""
Retargeting proof — a SECOND story on the SAME engine.
======================================================

`games/drowned-carillon/` is a self-contained game package: its own OKFS
knowledge bundle plus `bestiary.yaml` / `contracts.yaml` in the engine's schemas.
These tests prove the engine is retargetable by driving the *unchanged* engine
systems with that package's data:

* its `knowledge/` loads as its own `OKFSBundle` and validates clean;
* its bestiary feeds `resolve_combat` (including the sympathy "unmaking" path,
  which keys off the `clockwork` tag — same engine code, new data);
* its contracts feed `ContractBoard.available / accept / complete`.

Config is repointed via `get_config()._data['paths']` and the engine caches are
reset; fixtures restore both so the rest of the suite is unaffected.
"""

from __future__ import annotations

import random
from pathlib import Path

import pytest
import yaml

from engine.config import get_config
from engine.game.combat import load_bestiary, reset_bestiary_cache, resolve_combat
from engine.game.contracts import (
    ContractBoard,
    load_contracts,
    reset_contracts_cache,
)
from engine.game.state import GameState
from engine.okfs.bundle import OKFSBundle

# Repo root (this file lives in tests/) and the second-story package.
_ROOT = Path(__file__).resolve().parents[1]
_GAME = "games/drowned-carillon"
_KNOWLEDGE_DIR = _ROOT / _GAME / "knowledge"
_BESTIARY_REL = f"{_GAME}/data/bestiary.yaml"
_CONTRACTS_REL = f"{_GAME}/data/contracts.yaml"


# --------------------------------------------------------------------------
# Fixtures: repoint config + reset caches, then restore so other tests are safe.
# --------------------------------------------------------------------------
@pytest.fixture
def carillon_bestiary():
    """Point the engine's bestiary at the second story's foes."""
    cfg = get_config()
    paths = cfg._data.setdefault("paths", {})
    original = paths.get("bestiary")
    paths["bestiary"] = _BESTIARY_REL
    reset_bestiary_cache()
    try:
        yield
    finally:
        if original is None:
            paths.pop("bestiary", None)
        else:
            paths["bestiary"] = original
        reset_bestiary_cache()


@pytest.fixture
def carillon_contracts():
    """Point the engine's contract board at the second story's postings."""
    cfg = get_config()
    paths = cfg._data.setdefault("paths", {})
    original = paths.get("contracts")
    paths["contracts"] = _CONTRACTS_REL
    reset_contracts_cache()
    try:
        yield
    finally:
        if original is None:
            paths.pop("contracts", None)
        else:
            paths["contracts"] = original
        reset_contracts_cache()


# --------------------------------------------------------------------------
# 1. The knowledge bundle: same OKFS loader, its own root, validates clean.
# --------------------------------------------------------------------------
def test_second_bundle_validates_clean():
    bundle = OKFSBundle(_KNOWLEDGE_DIR)
    # Same loader, same validator: no missing frontmatter, no broken links.
    assert bundle.validate() == []
    # 7 self-contained concepts.
    assert len(bundle) == 7


def test_second_bundle_expected_concepts_and_types():
    bundle = OKFSBundle(_KNOWLEDGE_DIR)
    slugs = set(bundle.concepts)
    assert slugs == {
        "index",
        "the-drowned-carillon",
        "the-receding-tide",
        "brother-cael",
        "salt-widow-vesh",
        "bellfounders-quay",
        "the-sunken-nave",
    }
    # Required types are present, expressed in the engine's vocabulary.
    assert {c.slug for c in bundle.by_type("NPC")} == {"brother-cael", "salt-widow-vesh"}
    assert {c.slug for c in bundle.by_type("Location")} == {
        "bellfounders-quay",
        "the-sunken-nave",
    }
    assert {c.slug for c in bundle.by_type("Lore")} == {
        "the-drowned-carillon",
        "the-receding-tide",
    }
    # The threat concept names this story, not the flagship.
    threat = bundle.get("the-drowned-carillon")
    assert threat is not None and threat.type == "Lore"
    assert "Carillon" in threat.title


def test_second_bundle_links_resolve_within_itself():
    """Progressive disclosure works inside this sub-bundle (no cross-bundle leak)."""
    bundle = OKFSBundle(_KNOWLEDGE_DIR)
    # Every link in every concept resolves to a sibling here.
    for concept in bundle.concepts.values():
        for link in concept.links:
            assert link in bundle.concepts, f"{concept.slug} -> [[{link}]] unresolved"
    # The index reaches the threat and the hub by following links.
    index_neighbors = {c.slug for c in bundle.neighbors("index")}
    assert "the-drowned-carillon" in index_neighbors
    assert "bellfounders-quay" in index_neighbors


def test_second_bundle_does_not_pollute_main_bundle():
    """The second story is its own root; it shares nothing with knowledge/."""
    second = OKFSBundle(_KNOWLEDGE_DIR)
    main = OKFSBundle(_ROOT / "knowledge")
    # The flagship bundle does not contain this story's concepts.
    assert "the-drowned-carillon" not in main.concepts
    assert "bellfounders-quay" not in main.concepts
    # And the second story does not pull in flagship concepts.
    assert "the-clockwork-dark" not in second.concepts
    assert "maris-hearth" not in second.concepts


# --------------------------------------------------------------------------
# 2. Combat: the unchanged engine resolves fights against this story's foes.
# --------------------------------------------------------------------------
def test_engine_loads_second_story_bestiary(carillon_bestiary):
    bestiary = load_bestiary()
    assert set(bestiary) == {"ringing_gull", "chime_husk", "tide_cantor"}
    # Schema matches what the engine expects.
    cantor = bestiary["tide_cantor"]
    assert cantor["hp"] == 24
    assert "clockwork" in cantor["tags"]


def test_resolve_combat_defeats_second_story_foe(carillon_bestiary):
    """Drive real combat: attack the Tide-Cantor until the engine declares victory."""
    state = GameState()
    rng = random.Random(7)

    result = resolve_combat(state, "attack", target_id="tide_cantor", rng=rng)
    # The engine started THIS story's encounter.
    assert result.enemy_id == "tide_cantor"
    assert result.enemy_name == "The Tide-Cantor"

    # Keep swinging (high HP so we let the player win for the proof).
    for _ in range(60):
        if state.combat is None:
            break
        # Top up so a defeat respawn doesn't end the loop prematurely.
        if state.stats.hp < 6:
            state.stats.hp = state.stats.max_hp
        result = resolve_combat(state, "attack", rng=rng)

    assert result.victory is True
    assert result.enemy_id == "tide_cantor"
    # Victory loot is THIS story's drop, granted by the engine.
    assert any(i.id == "tuning_fork" for i in state.inventory)
    assert state.combat is None


def test_sympathy_unmakes_clockwork_tagged_carillon_foe(carillon_bestiary):
    """The `clockwork` tag still routes to the engine's sympathy 'unmaking' path."""
    state = GameState()
    state.stats.focus = 10  # enough to pay the sympathy cost and roll well
    rng = random.Random(3)

    # Start the encounter against a clockwork-tagged chime-husk.
    resolve_combat(state, "attack", target_id="chime_husk", rng=rng)
    assert state.combat is not None
    assert "clockwork" in state.combat["enemy"]["tags"]

    saw_unmake = False
    for _ in range(40):
        if state.combat is None:
            break
        state.stats.focus = max(state.stats.focus, 8)  # keep sympathy affordable
        if state.stats.hp < 6:
            state.stats.hp = state.stats.max_hp
        result = resolve_combat(state, "sympathy", rng=rng)
        if result.outcome == "sympathy_unmake":
            saw_unmake = True
    assert saw_unmake, "engine never routed a clockwork foe to the unmaking path"


# --------------------------------------------------------------------------
# 3. Contracts: the unchanged ContractBoard runs this story's notice board.
# --------------------------------------------------------------------------
def test_engine_loads_second_story_contracts(carillon_contracts):
    catalogue = load_contracts()
    assert set(catalogue) == {
        "still_the_carillon",
        "carry_the_lamp_oil",
        "bounty_tide_cantor",
    }
    assert catalogue["still_the_carillon"]["kind"] == "anti_dark"


def test_contract_board_available_accept_complete(carillon_contracts):
    """Full engine-authoritative cycle on THIS story's anti-dark contract."""
    state = GameState()
    state.location_id = "bellfounders_quay"  # this story's hub id

    # available(): the gated bounty (min_awareness 20) is hidden at 0 awareness.
    offered = {c["id"] for c in ContractBoard.available(state)}
    assert "still_the_carillon" in offered
    assert "carry_the_lamp_oil" in offered
    assert "bounty_tide_cantor" not in offered

    # accept()
    accepted = ContractBoard.accept(state, "still_the_carillon")
    assert accepted["success"] is True
    assert accepted["status"] == "accepted"
    assert any(c["id"] == "still_the_carillon" for c in state.contracts)

    gold_before = state.stats.gold

    # complete(): the engine grants THIS story's reward.
    done = ContractBoard.complete(state, "still_the_carillon")
    assert done["success"] is True
    assert done["status"] == "complete"
    reward = done["reward"]
    # gold + engagement + reputation for Brother Cael, all engine-applied.
    assert state.stats.gold == gold_before + 10
    assert "engagement" in reward
    assert state.reputations.get("npc_cael", 0) == 2


def test_gated_bounty_opens_with_awareness(carillon_contracts):
    """The engine's min_awareness gate works on this story's data unchanged."""
    state = GameState()
    state.location_id = "bellfounders_quay"
    state.awareness = 25.0  # clears the bounty's min_awareness: 20 gate

    offered = {c["id"] for c in ContractBoard.available(state)}
    assert "bounty_tide_cantor" in offered

    assert ContractBoard.accept(state, "bounty_tide_cantor")["success"] is True
    done = ContractBoard.complete(state, "bounty_tide_cantor")
    assert done["success"] is True
    # Bounty item reward is granted by the engine.
    assert any(i.id == "salvaged_brass" for i in state.inventory)
