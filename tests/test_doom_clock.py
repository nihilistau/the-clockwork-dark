"""The Doom Clock — arcs, beats, engagement, consumed ending (PR28)."""

from __future__ import annotations

import random

from engine.game.combat import resolve_combat
from engine.game.doom_clock import (
    ARC_CONSUMED,
    ARC_CONVERGENCE,
    ARC_MARCH,
    ARC_QUIET,
    ARC_WHISPER,
    DoomClock,
)
from engine.game.evil_ticker import EvilTicker
from engine.game.state import EvilPhase, GameState
from engine.okfs import get_bundle, reset_bundle


class _MaxRng(random.Random):
    def randint(self, a, b):  # type: ignore[override]
        return b


def test_arc_transitions():
    assert DoomClock.arc(GameState()) == ARC_QUIET
    assert DoomClock.arc(GameState(awareness=22.0)) == ARC_WHISPER
    assert DoomClock.arc(GameState(awareness=30.0)) == ARC_MARCH
    s = GameState()
    s.evil_phase = EvilPhase.SPREADING
    assert DoomClock.arc(s) == ARC_CONVERGENCE
    s2 = GameState(evil_progress=1.0)
    assert DoomClock.arc(s2) == ARC_CONSUMED


def test_pending_beats_once_only():
    s = GameState(evil_progress=0.5)
    first = DoomClock.pending_beats(s)
    ids = [b.id for b in first]
    assert ids == ["harvest_south", "scarecrow_wakes", "vines_breach_forest"]
    assert DoomClock.pending_beats(s) == []  # already seen


def test_tunnels_beat_carries_cutscene():
    s = GameState(evil_progress=0.7)
    beats = {b.id: b for b in DoomClock.pending_beats(s)}
    assert "tunnels_open" in beats
    assert beats["tunnels_open"].cutscene_id == "cutscene_hidden_tunnel"


def test_consumed_ends_the_game():
    s = GameState(evil_progress=1.0)
    beats = DoomClock.pending_beats(s)
    assert any(b.id == "consumed" for b in beats)
    assert s.ended is True
    assert s.flags.get("consumed") is True


def test_engagement_caps_and_registers():
    s = GameState()
    assert DoomClock.register_engagement(s, 8.0) == 8.0
    DoomClock.register_engagement(s, 200.0)
    assert s.engagement == 100.0


def test_engagement_slows_the_clock():
    base = GameState(location_id="edgewood_square")
    held = GameState(location_id="edgewood_square")
    held.engagement = 100.0
    EvilTicker.advance(base, days_elapsed=1.0)
    EvilTicker.advance(held, days_elapsed=1.0)
    assert held.evil_progress < base.evil_progress  # engaged player holds the line


def test_clockwork_victory_raises_engagement():
    s = GameState()
    before = s.engagement
    # clockwork_beast is tagged "clockwork"; max rolls one-shot toward victory
    res = None
    for _ in range(8):
        res = resolve_combat(s, "attack", target_id="clockwork_beast", rng=_MaxRng())
        if res.ended:
            break
    assert res is not None and res.victory
    assert s.engagement > before


def test_snapshot_fields():
    s = GameState(evil_progress=0.3, awareness=22.0)
    DoomClock.pending_beats(s)
    snap = DoomClock.snapshot(s)
    assert snap["arc"] == ARC_WHISPER
    assert "latest_beat" in snap
    assert "engagement" in snap


def test_story_concepts_validate():
    reset_bundle()
    bundle = get_bundle(force=True)
    for slug in ("the-two-powers", "the-harvest", "doom-arcs"):
        c = bundle.get(slug)
        assert c is not None and c.type == "Lore"
    assert bundle.validate() == []
