"""March arc travel gating + cutscene milestones (PR15, v0.2)."""

from __future__ import annotations

import pytest

from engine.media.milestones import CutsceneMilestones
from engine.game.state import EvilPhase, GameState
from engine.world.content import (
    location_accessible,
    reset_content_cache,
    travel_edge_allowed,
)


@pytest.fixture(autouse=True)
def _reset():
    reset_content_cache()
    yield
    reset_content_cache()


# --- March-arc travel gating (Awareness >= 25 OR evil >= SPREADING) ---------

def test_marches_locked_when_low_awareness_and_dormant():
    ok, reason = location_accessible("marches_road", evil_phase="dormant", awareness=0.0)
    assert ok is False
    assert "awareness" in reason.lower() or "spreading" in reason.lower()


def test_marches_open_via_awareness():
    ok, _ = location_accessible("marches_road", evil_phase="dormant", awareness=25.0)
    assert ok is True


def test_marches_open_via_phase():
    ok, _ = location_accessible("marches_road", evil_phase="spreading", awareness=0.0)
    assert ok is True


def test_edge_to_marches_respects_awareness_gate():
    blocked, _ = travel_edge_allowed(
        "resting_camp", "marches_road", evil_phase="dormant", awareness=0.0
    )
    assert blocked is False
    allowed, _ = travel_edge_allowed(
        "resting_camp", "marches_road", evil_phase="dormant", awareness=30.0
    )
    assert allowed is True


def test_millhaven_reachable_from_marches():
    # millhaven_gate itself has no extra gate; reachable once on the marches.
    ok, _ = location_accessible("millhaven_gate", evil_phase="dormant", awareness=30.0)
    assert ok is True


def test_phase_only_gate_ignores_awareness():
    # corruption_border edge is phase-gated (min_phase spreading), no awareness unlock.
    blocked, _ = travel_edge_allowed(
        "marches_road", "corruption_border", evil_phase="dormant", awareness=99.0
    )
    assert blocked is False


# --- Cutscene milestones ----------------------------------------------------

def _state(phase: EvilPhase, awareness: float = 0.0) -> GameState:
    s = GameState()
    s.evil_phase = phase
    s.awareness = awareness
    return s


def test_no_milestone_in_dormant():
    assert CutsceneMilestones.due_milestone(_state(EvilPhase.DORMANT)) is None


def test_stirring_milestone_due():
    m = CutsceneMilestones.due_milestone(_state(EvilPhase.STIRRING))
    assert m is not None and m.cutscene_id == "cutscene_stirring_phase"


def test_assistant_reveal_via_awareness():
    # awareness >= reflection_form_min (40), still dormant so stirring not due
    m = CutsceneMilestones.due_milestone(_state(EvilPhase.DORMANT, awareness=45.0))
    assert m is not None and m.cutscene_id == "cutscene_assistant_reveal"


def test_consuming_milestone_due():
    s = _state(EvilPhase.CONSUMING)
    s.flags["milestone_stirring"] = True  # already fired earlier
    m = CutsceneMilestones.due_milestone(s)
    assert m is not None and m.cutscene_id == "cutscene_consuming_horizon"


def test_trigger_fires_once_and_sets_flag():
    s = _state(EvilPhase.STIRRING)
    job = CutsceneMilestones.trigger(s, force=True)
    assert job is not None
    assert s.flags.get("milestone_stirring") is True
    assert "stirring" in (job.payload.get("cutscene_id", ""))
    # second call: already fired, nothing due (same phase)
    assert CutsceneMilestones.trigger(s, force=True) is None


def test_budget_block_leaves_flag_unset_for_retry():
    s = _state(EvilPhase.STIRRING)
    # Simulate a cutscene already shown this phase so the budget blocks.
    s.last_cutscene_phase = "stirring"
    s.media_cutscenes_shown = ["something"]
    job = CutsceneMilestones.trigger(s, force=False)
    assert job is None
    assert s.flags.get("milestone_stirring") is None  # will retry next phase shift
