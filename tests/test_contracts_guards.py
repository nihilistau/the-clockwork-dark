"""Contract accept/complete guards + reward branches (gap closure).

Complements test_contracts.py: double-complete is idempotent (no second
reward), accept rejects unknown / already-taken / gated postings, and the
item/awareness/hp reward branches in ``_apply_reward`` are exercised.
"""

from __future__ import annotations

import pytest

from engine.game.contracts import ContractBoard, reset_contracts_cache
from engine.game.state import EvilPhase, GameState


@pytest.fixture(autouse=True)
def _reset():
    reset_contracts_cache()
    yield
    reset_contracts_cache()


# --- complete is idempotent -------------------------------------------------

def test_complete_twice_does_not_reapply_reward():
    s = GameState(location_id="edgewood_square")
    s.stats.gold = 0
    assert ContractBoard.accept(s, "still_south_harvester")["success"]

    first = ContractBoard.complete(s, "still_south_harvester")
    assert first["success"]
    gold_after_first = s.stats.gold
    eng_after_first = s.engagement
    assert gold_after_first == 8  # reward applied once

    second = ContractBoard.complete(s, "still_south_harvester")
    assert second["success"] is False
    assert second["message"] == "Already settled."
    # nothing re-applied on the second attempt
    assert s.stats.gold == gold_after_first
    assert s.engagement == eng_after_first


# --- accept failure modes ---------------------------------------------------

def test_accept_unknown_contract_fails():
    s = GameState(location_id="edgewood_square")
    res = ContractBoard.accept(s, "no_such_contract")
    assert res["success"] is False
    assert "No such contract" in res["message"]
    assert s.contracts == []


def test_accept_already_taken_fails():
    s = GameState(location_id="edgewood_square")
    assert ContractBoard.accept(s, "still_south_harvester")["success"]
    again = ContractBoard.accept(s, "still_south_harvester")
    assert again["success"] is False
    assert again["message"] == "Already on your slate."
    # still only one entry on the slate
    assert len(s.contracts) == 1


def test_accept_gated_contract_fails_until_threshold():
    # bounty_brass_scarecrow requires awareness >= 20.
    s = GameState(location_id="edgewood_square", awareness=0.0)
    gated = ContractBoard.accept(s, "bounty_brass_scarecrow")
    assert gated["success"] is False
    assert "isn't open to you yet" in gated["message"]
    assert s.contracts == []

    s.awareness = 25.0
    ok = ContractBoard.accept(s, "bounty_brass_scarecrow")
    assert ok["success"] is True


# --- reward branches: item / awareness / hp --------------------------------

def test_item_reward_branch_grants_inventory_item():
    s = GameState(location_id="edgewood_square", awareness=25.0)
    assert ContractBoard.accept(s, "bounty_brass_scarecrow")["success"]
    done = ContractBoard.complete(s, "bounty_brass_scarecrow")
    assert done["success"]
    assert done["reward"].get("item", {}).get("id") == "brass_filings"
    assert any(i.id == "brass_filings" for i in s.inventory)


def test_awareness_reward_branch_raises_awareness():
    # ilya_2_read_the_road rewards awareness: 4 (and is itself awareness-gated).
    s = GameState(location_id="tinker_caravan", awareness=20.0)
    assert ContractBoard.accept(s, "ilya_2_read_the_road")["success"]
    before = s.awareness
    done = ContractBoard.complete(s, "ilya_2_read_the_road")
    assert done["success"]
    assert s.awareness == before + 4
    assert done["reward"]["awareness"] == s.awareness


def test_hp_reward_branch_clamps_to_max():
    # No catalogue contract grants hp, so exercise the branch directly.
    s = GameState()
    s.stats.hp = 5
    s.stats.max_hp = 20
    applied = ContractBoard._apply_reward(s, {"hp": 50})
    assert s.stats.hp == 20  # clamped to max_hp
    assert applied["hp"] == 20

    # and a negative delta floors at 0
    floored = ContractBoard._apply_reward(s, {"hp": -999})
    assert s.stats.hp == 0
    assert floored["hp"] == 0
