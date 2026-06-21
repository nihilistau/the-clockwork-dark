"""
Set-piece tests — the tunnel-mouth descent
==========================================

An authored, gated, engine-adjudicated decision_tree. Sealed until the world has
opened its ground (the tunnels_open beat); the engine owns every branch and
outcome. See engine/game/set_pieces.py, data/set_pieces.yaml, [[the-tunnel-mouth]].
"""

from __future__ import annotations

import pytest

from engine.game.challenges import resolve_challenge
from engine.game.set_pieces import reset_set_pieces_cache, start_set_piece
from engine.game.state import GameState


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


def test_set_piece_sealed_until_the_world_opens_it():
    s = GameState()  # tunnels not open
    res = start_set_piece(s, "tunnel_mouth")
    assert res.status == "error"
    assert s.challenge is None


def test_unknown_set_piece_is_error():
    assert start_set_piece(_opened(), "no_such_place").status == "error"


def test_tunnel_mouth_opens_with_scene_art_and_clue():
    s = _opened()
    res = start_set_piece(s, "tunnel_mouth")
    assert res.status == "active"
    assert s.challenge is not None
    assert s.challenge["kind"] == "decision_tree"
    assert s.challenge["current"] == "descend"
    node = s.challenge["nodes"]["descend"]
    assert node["image"].startswith("assets/Tunnels/")
    assert node.get("riddle")


def test_seal_path_succeeds_sets_flag_and_grants_key():
    s = _opened()
    start_set_piece(s, "tunnel_mouth")
    assert resolve_challenge(s, choice="enter").status == "active"   # -> fork_ab
    assert resolve_challenge(s, choice="a").status == "active"       # -> junction_def
    assert resolve_challenge(s, choice="d").status == "active"       # -> chamber_gh
    final = resolve_challenge(s, choice="jam")                       # -> t_sealed
    assert final.status == "success"
    assert s.flags.get("tunnel_sealed") is True
    assert s.engagement > 0
    assert any(i.id == "iron_key" for i in s.inventory)
    assert s.challenge is None  # consumed


def test_collapse_path_fails_and_hurts():
    s = _opened()
    s.stats.hp = 20
    start_set_piece(s, "tunnel_mouth")
    resolve_challenge(s, choice="enter")            # -> fork_ab
    resolve_challenge(s, choice="b")                # -> clockface
    final = resolve_challenge(s, choice="press")    # -> t_collapse
    assert final.status == "failure"
    assert s.stats.hp < 20
    assert s.challenge is None


def test_relic_path_grants_item_but_leaves_seam_open():
    s = _opened()
    start_set_piece(s, "tunnel_mouth")
    resolve_challenge(s, choice="read")    # -> read_carvings
    resolve_challenge(s, choice="down")    # -> fork_ab
    resolve_challenge(s, choice="a")       # -> junction_def
    resolve_challenge(s, choice="d")       # -> chamber_gh
    final = resolve_challenge(s, choice="take")  # -> t_relic
    assert final.status == "success"
    assert any(i.id == "old_clock_part" for i in s.inventory)
    assert s.flags.get("tunnel_sealed") is not True  # seam stays open
