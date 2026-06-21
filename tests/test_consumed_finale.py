"""The 'consumed' terminal — evil_progress 1.0 with no intervention ends the game.

Drives the real ``clockwork_state.run_turn`` with evil_progress pinned at 1.0
and asserts the Doom Clock fires the once-only ``consumed`` beat, flags the
state consumed/ended, appends the beat text to the narration, and reports it in
the ``doom`` snapshot.
"""

from __future__ import annotations

import pytest

from content.scenes.clockwork.clockwork_state import GameSession, run_turn
from engine.agents.assistant import AssistantAgent
from engine.agents.storyteller import StorytellerAgent
from engine.game.doom_clock import DoomClock
from engine.game.engine import GameEngine, set_active_engine
from engine.game.state import EvilPhase, GameState
from engine.governance import reset_governance


@pytest.fixture(autouse=True)
def _reset_gov():
    reset_governance()
    yield
    reset_governance()


QUIET_TURN = (
    '{"narration": "Smoke threads the grey above the bakery roof; the ovens are '
    'still warm and the street is very quiet this hour of the morning.",'
    ' "choices": [{"id":"a","text":"Walk on"},{"id":"b","text":"Wait"}],'
    ' "tool_calls": []}'
)


def _consumed_session() -> GameSession:
    state = GameState(evil_progress=1.0)
    state.evil_phase = EvilPhase.CONSUMING
    eng = GameEngine(state)
    set_active_engine(eng)
    llm = lambda _m: QUIET_TURN  # noqa: E731
    return GameSession(
        engine=eng,
        storyteller=StorytellerAgent(eng, llm_fn=llm),
        assistant=AssistantAgent(eng, llm_fn=llm),
    )


def test_consumed_terminal_ends_the_game():
    session = _consumed_session()
    state = session.engine.state

    turn = run_turn(session, "do nothing in particular")

    # the once-only consumed beat fired this turn
    consumed_beat = next((b for b in turn["doom_beats"] if b["id"] == "consumed"), None)
    assert consumed_beat is not None, turn["doom_beats"]

    # terminal flags set on the state
    assert state.flags.get("consumed") is True
    assert state.ended is True
    assert "consumed" in state.doom_beats_seen

    # the consumed beat's prose is appended to the narration
    assert consumed_beat["text"] in turn["narration"]

    # the doom snapshot reflects the terminal and the convergence layer is closed
    doom = turn["doom"]
    assert doom["consumed"] is True
    assert doom["arc"] == "consumed"
    # convergence is closed once consumed; no reckoning outcome was recorded
    assert doom["convergence"]["open"] is False
    assert doom["convergence"]["outcome"] == ""


def test_consumed_beat_is_once_only():
    session = _consumed_session()
    run_turn(session, "first")
    # second turn: the beat does not re-fire (already in doom_beats_seen)
    turn2 = run_turn(session, "second")
    assert all(b["id"] != "consumed" for b in turn2["doom_beats"])
    # but the snapshot still reports the world as consumed
    assert turn2["doom"]["consumed"] is True


def test_pending_beats_marks_consumed_directly():
    """Unit-level guard on the DoomClock terminal (independent of the turn loop)."""
    state = GameState(evil_progress=1.0)
    beats = DoomClock.pending_beats(state)
    assert any(b.id == "consumed" for b in beats)
    assert state.ended is True and state.flags["consumed"] is True
