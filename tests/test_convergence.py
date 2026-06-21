"""The convergence finale — approach beats + the last engine-resolved choice."""

from __future__ import annotations

import json
import random

from engine.game.doom_clock import (
    CONVERGENCE_THRESHOLD,
    RECKONING_BEATS,
    Convergence,
    DoomClock,
)
from engine.game.engine import GameEngine, set_active_engine
from engine.game.state import EvilPhase, GameState
from engine.okfs import get_bundle, reset_bundle
from engine.skills.registry import SKILL_REGISTRY
import engine.skills.builtin.mechanics  # noqa: F401  (registers skills)


class _MaxRng(random.Random):
    def randint(self, a, b):  # type: ignore[override]
        return b


class _MinRng(random.Random):
    def randint(self, a, b):  # type: ignore[override]
        return a


def _late_state(progress: float = 0.85) -> GameState:
    s = GameState(evil_progress=progress)
    s.evil_phase = EvilPhase.CONSUMING
    return s


# --- gating -----------------------------------------------------------------

def test_convergence_closed_early():
    assert Convergence.is_open(GameState()) is False
    assert Convergence.is_open(GameState(evil_progress=0.5)) is False


def test_convergence_opens_at_threshold():
    s = _late_state(CONVERGENCE_THRESHOLD)
    assert Convergence.is_open(s) is True


def test_convergence_closed_once_consumed():
    s = _late_state(1.0)
    assert Convergence.is_open(s) is False  # already consumed; no finale to run


# --- approach beats are once-only and ordered ------------------------------

def test_reckoning_beats_fire_in_order_once():
    s = _late_state()
    first = Convergence.pending_reckoning_beats(s)
    assert [b.id for b in first] == [b.id for b in RECKONING_BEATS]
    assert Convergence.pending_reckoning_beats(s) == []  # already seen


def test_reckoning_beats_reuse_existing_cutscenes():
    ids = {b.cutscene_id for b in RECKONING_BEATS if b.cutscene_id}
    assert "cutscene_tower" in ids
    assert "cutscene_consuming_horizon" in ids


# --- the last engine-resolved choice ---------------------------------------

def test_walk_away_always_succeeds_and_ends():
    s = _late_state()
    res = Convergence.resolve_reckoning(s, "walk_away")
    assert res.success and res.outcome == "walked_away"
    assert s.ended is True and s.flags.get("walked_away") is True
    assert s.evil_progress < 1.0  # not force-consumed


def test_stand_holds_the_line_on_a_good_roll():
    s = _late_state(0.85)
    s.engagement = 100.0
    res = Convergence.resolve_reckoning(s, "stand", rng=_MaxRng())
    assert res.success and res.outcome == "held"
    assert s.ended is True and s.flags.get("reckoning_held") is True
    assert s.evil_progress < 1.0  # held, never force-consumed


def test_unmake_can_fail_on_a_bad_roll():
    s = _late_state(0.99)  # high DC
    s.engagement = 0.0     # no bonus
    res = Convergence.resolve_reckoning(s, "unmake", rng=_MinRng())
    assert res.success is False and res.outcome == "not_enough"
    assert s.flags.get("reckoning_failed") is True
    # failure does NOT force-consume; the existing terminal falls on its own time
    assert s.ended is False


def test_reckoning_dc_scales_with_progress():
    near = Convergence.reckoning_dc(_late_state(CONVERGENCE_THRESHOLD))
    far = Convergence.reckoning_dc(_late_state(0.99))
    assert far > near


def test_reckoning_rejected_before_open():
    s = GameState()  # quiet life
    res = Convergence.resolve_reckoning(s, "stand")
    assert res.success is False and res.outcome == "not_open"
    assert s.ended is False


def test_invalid_choice_rejected():
    s = _late_state()
    res = Convergence.resolve_reckoning(s, "negotiate")
    assert res.success is False and res.outcome == "invalid"


# --- snapshot wiring + skills ----------------------------------------------

def test_doom_snapshot_includes_convergence():
    s = _late_state()
    snap = DoomClock.snapshot(s)
    assert "convergence" in snap
    assert snap["convergence"]["open"] is True


def test_resolve_reckoning_skill():
    s = _late_state()
    s.engagement = 100.0
    set_active_engine(GameEngine(s))
    raw = SKILL_REGISTRY.invoke("resolve_reckoning", choice="walk_away")
    data = json.loads(raw)
    assert data["success"] is True
    assert data["outcome"] == "walked_away"


def test_query_convergence_skill():
    s = _late_state()
    set_active_engine(GameEngine(s))
    raw = SKILL_REGISTRY.invoke("query_convergence")
    data = json.loads(raw)
    assert data["open"] is True
    assert data["reckoning_dc"] > 0
    assert isinstance(data["pending_beats"], list)


# --- new lore concepts validate --------------------------------------------

def test_world_expansion_lore_validates():
    reset_bundle()
    bundle = get_bundle(force=True)
    for slug in (
        "the-heartlands", "the-tinkers", "beneath-the-tunnels",
        "sympathy-and-naming", "the-convergence", "the-tinkers-questline",
    ):
        c = bundle.get(slug)
        assert c is not None and c.type == "Lore", f"missing or mistyped: {slug}"
    assert bundle.validate() == []
