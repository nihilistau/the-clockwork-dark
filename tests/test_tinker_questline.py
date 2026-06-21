"""The Tinker's Reckoning — Ilya's contract chain (engine-granted rewards)."""

from __future__ import annotations

from engine.game.contracts import ContractBoard, load_contracts, reset_contracts_cache
from engine.game.state import EvilPhase, GameState


def setup_function() -> None:
    reset_contracts_cache()


def teardown_function() -> None:
    reset_contracts_cache()


CHAIN = [
    "ilya_1_gather_filings",
    "ilya_2_read_the_road",
    "ilya_3_the_naming_lamp",
    "ilya_4_what_ilya_is",
]


def test_chain_present_and_given_by_ilya():
    cat = load_contracts()
    for cid in CHAIN:
        assert cid in cat, f"missing contract {cid}"
        assert cat[cid]["giver"] == "npc_ilya"
    # the capstone steps push back against the Dark
    assert cat["ilya_3_the_naming_lamp"]["kind"] == "anti_dark"
    assert cat["ilya_4_what_ilya_is"]["kind"] == "anti_dark"


def test_first_step_available_at_caravan():
    state = GameState(location_id="tinker_caravan")
    available = {c["id"] for c in ContractBoard.available(state)}
    assert "ilya_1_gather_filings" in available
    # later steps are gated by awareness/phase, not yet open
    assert "ilya_3_the_naming_lamp" not in available


def test_completing_first_step_grants_reward():
    state = GameState(location_id="tinker_caravan")
    gold_before = state.stats.gold
    ContractBoard.accept(state, "ilya_1_gather_filings")
    res = ContractBoard.complete(state, "ilya_1_gather_filings")
    assert res["success"] is True
    assert state.stats.gold > gold_before
    assert any(i.id == "brass_filings" for i in state.inventory)
    assert state.reputations.get("npc_ilya", 0) >= 2


def test_anti_dark_capstone_raises_engagement():
    state = GameState(location_id="tinker_caravan", awareness=35.0)
    state.evil_phase = EvilPhase.SPREADING
    # the naming-lamp step is gated to stirring+/awareness 25+ — open here
    available = {c["id"] for c in ContractBoard.available(state)}
    assert "ilya_3_the_naming_lamp" in available
    ContractBoard.accept(state, "ilya_3_the_naming_lamp")
    before = state.engagement
    res = ContractBoard.complete(state, "ilya_3_the_naming_lamp")
    assert res["success"] is True
    assert state.engagement > before
    assert any(i.id == "sympathy_lamp" for i in state.inventory)
