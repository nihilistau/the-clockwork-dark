"""
The Warden's Barrow set-piece + its convergence payoff
======================================================

Reachable once the tunnels open the hidden path. Reading the standing stones
gives the older name (the Hollow Crown); naming it at the star-chart sets
``knows_older_name``, which sharpens the *unmake* reckoning at the tower. See
data/set_pieces.yaml, engine/game/doom_clock.py, [[the-first-warden]].
"""

from __future__ import annotations

import pytest

from engine.game.challenges import resolve_challenge
from engine.game.doom_clock import (
    CONVERGENCE_THRESHOLD,
    RECKONING_UNMAKE,
    Convergence,
)
from engine.game.set_pieces import reset_set_pieces_cache, start_set_piece
from engine.game.state import GameState


class _FixedRng:
    """Deterministic d20 — every randint returns the same nat roll."""

    def __init__(self, value: int) -> None:
        self.value = value

    def randint(self, _a: int, _b: int) -> int:
        return self.value


@pytest.fixture(autouse=True)
def _fresh():
    reset_set_pieces_cache()
    yield
    reset_set_pieces_cache()


def _opened() -> GameState:
    s = GameState()
    s.flags["tunnels_open"] = True
    s.flags["discovery_hidden_path"] = True
    return s


def test_barrow_sealed_until_the_path_is_open():
    s = GameState()  # hidden_path not discovered
    assert start_set_piece(s, "warden_barrow").status == "error"
    assert s.challenge is None


def test_read_stones_then_name_the_crown_learns_the_older_name():
    s = _opened()
    start_set_piece(s, "warden_barrow")
    assert resolve_challenge(s, choice="read").status == "active"   # -> read_stones
    assert resolve_challenge(s, choice="enter").status == "active"  # -> hall_clued
    assert resolve_challenge(s, choice="map").status == "active"    # -> star_map_clued
    final = resolve_challenge(s, choice="crown")                    # -> t_older_name
    assert final.status == "success"
    assert s.flags.get("knows_older_name") is True
    assert any(i.id == "older_name" for i in s.inventory)
    assert s.engagement > 0
    assert s.challenge is None


def test_trusting_the_faceless_assistant_gets_the_wrong_name():
    s = _opened()
    start_set_piece(s, "warden_barrow")
    resolve_challenge(s, choice="enter")   # -> hall_blind (didn't read the stones)
    resolve_challenge(s, choice="map")     # -> star_map_blind
    s.stats.hp = 20
    final = resolve_challenge(s, choice="trust")  # the figure misleads -> t_wrong_name
    assert final.status == "failure"
    assert s.flags.get("knows_older_name") is not True
    assert s.stats.hp < 20


def test_raising_a_hand_against_the_warden_husk_hurts():
    s = _opened()
    s.stats.hp = 20
    start_set_piece(s, "warden_barrow")
    resolve_challenge(s, choice="enter")          # -> hall_blind
    final = resolve_challenge(s, choice="fight")  # -> t_husk_hurt
    assert final.status == "failure"
    assert s.stats.hp < 20


def _converged() -> GameState:
    s = GameState()
    s.evil_progress = CONVERGENCE_THRESHOLD  # finale open, reckoning DC == base (12)
    return s


def test_older_name_sharpens_the_unmake_reckoning():
    # A nat-8 roll with no engagement: total 8 < DC 12 normally, 8+5 = 13 >= 12
    # once the older name is known. The barrow discovery is a real edge at the end.
    without = _converged()
    lost = Convergence.resolve_reckoning(without, RECKONING_UNMAKE, rng=_FixedRng(8))
    assert lost.success is False

    knowing = _converged()
    knowing.flags["knows_older_name"] = True
    won = Convergence.resolve_reckoning(knowing, RECKONING_UNMAKE, rng=_FixedRng(8))
    assert won.success is True
    assert won.outcome == "held"


def test_older_name_does_not_help_a_plain_stand():
    # The edge is specific to unmaking (naming turned back) — not to standing firm.
    s = _converged()
    s.flags["knows_older_name"] = True
    res = Convergence.resolve_reckoning(s, "stand", rng=_FixedRng(8))
    assert res.success is False  # no older-name bonus on a stand
