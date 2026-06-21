"""Notice board & contracts (v0.6)."""

from __future__ import annotations

import json

import pytest

from engine.game.contracts import ContractBoard, load_contracts, reset_contracts_cache
from engine.game.engine import GameEngine, set_active_engine
from engine.game.state import GameState
from engine.skills.registry import SKILL_REGISTRY
import engine.skills.builtin.contracts  # noqa: F401


@pytest.fixture(autouse=True)
def _reset():
    reset_contracts_cache()
    yield
    reset_contracts_cache()


def test_catalogue_loads():
    cat = load_contracts()
    assert "still_south_harvester" in cat
    assert cat["still_south_harvester"]["kind"] == "anti_dark"


def test_available_filtered_by_location():
    s = GameState(location_id="edgewood_square")
    ids = {c["id"] for c in ContractBoard.available(s)}
    assert "still_south_harvester" in ids       # noticeboard @ square
    assert "tinkers_lost_cog" not in ids        # only at tinker_caravan


def test_available_gated_by_awareness():
    s = GameState(location_id="edgewood_square", awareness=0.0)
    ids = {c["id"] for c in ContractBoard.available(s)}
    assert "bounty_brass_scarecrow" not in ids  # needs awareness >= 20
    s.awareness = 25.0
    ids = {c["id"] for c in ContractBoard.available(s)}
    assert "bounty_brass_scarecrow" in ids


def test_accept_and_complete_applies_reward():
    s = GameState(location_id="edgewood_square")
    s.stats.gold = 0
    acc = ContractBoard.accept(s, "still_south_harvester")
    assert acc["success"] and s.contracts[0]["status"] == "accepted"
    # no longer offered once taken
    assert "still_south_harvester" not in {c["id"] for c in ContractBoard.available(s)}
    done = ContractBoard.complete(s, "still_south_harvester")
    assert done["success"]
    assert s.stats.gold == 8
    assert s.engagement == 12
    assert s.reputations.get("npc_sera") == 2
    assert s.contracts[0]["status"] == "complete"


def test_complete_requires_accept():
    s = GameState()
    res = ContractBoard.complete(s, "still_south_harvester")
    assert res["success"] is False


def test_contracts_persist_save_round_trip():
    s = GameState(location_id="edgewood_square")
    ContractBoard.accept(s, "still_south_harvester")
    restored = GameState.from_dict(s.to_dict())
    assert restored.contracts and restored.contracts[0]["id"] == "still_south_harvester"


def test_contract_skills_via_registry():
    s = GameState(location_id="edgewood_bakery")
    eng = GameEngine(s)
    set_active_engine(eng)
    avail = json.loads(SKILL_REGISTRY.invoke("list_contracts"))
    assert any(c["id"] == "deliver_dawn_bread" for c in avail["available"])
    acc = json.loads(SKILL_REGISTRY.invoke("accept_contract", contract_id="deliver_dawn_bread"))
    assert acc["success"]
    done = json.loads(SKILL_REGISTRY.invoke("complete_contract", contract_id="deliver_dawn_bread"))
    assert done["success"] and s.stats.gold >= 3


def test_notice_board_lore_validates():
    from engine.okfs import get_bundle, reset_bundle

    reset_bundle()
    bundle = get_bundle(force=True)
    assert bundle.get("the-notice-board") is not None
    assert bundle.validate() == []
