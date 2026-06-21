"""Governance surfaced through the real clockwork turn (gap: R003 in turn_update).

Drives ``clockwork_state.run_turn`` exactly as the route/socket do, with a mock
LLM that claims an UNRECEIPTED ``stat_changes`` delta. The RulesGovernor must
record an R003-type violation, and it must reach the ``governance`` field of the
``turn_update`` payload.
"""

from __future__ import annotations

import pytest

from content.scenes.clockwork.clockwork_state import GameSession, run_turn
from engine.agents.assistant import AssistantAgent
from engine.agents.storyteller import StorytellerAgent
from engine.game.engine import GameEngine, set_active_engine
from engine.game.state import GameState
from engine.governance import reset_governance


@pytest.fixture(autouse=True)
def _reset_gov():
    reset_governance()
    yield
    reset_governance()


# An LLM that narrates an hp loss and *claims* it in stat_changes with no roll.
UNRECEIPTED_STAT = (
    '{"narration": "The cold bites and your old wound reopens in the mist; '
    'the road blurs before your eyes for a long, grey moment.",'
    ' "choices": [{"id":"a","text":"Press on"},{"id":"b","text":"Rest a while"}],'
    ' "tool_calls": [], "stat_changes": {"hp": -6}}'
)


def _session(llm_fn) -> GameSession:
    eng = GameEngine(GameState())
    set_active_engine(eng)
    return GameSession(
        engine=eng,
        storyteller=StorytellerAgent(eng, llm_fn=llm_fn),
        assistant=AssistantAgent(eng, llm_fn=llm_fn),
    )


def test_run_turn_surfaces_r003_in_turn_update():
    session = _session(lambda _m: UNRECEIPTED_STAT)
    turn = run_turn(session, "wander into the cold")

    gov = turn["governance"]
    assert any(v["rule_id"] == "R003" for v in gov), gov
    # the engine never actually applied the claimed delta (stats only move via skills)
    assert turn["state"]["stats"]["hp"] == session.engine.state.stats.max_hp


def test_run_turn_governance_emitted_over_callback():
    """The same payload (governance included) is what the socket emit_callback sends."""
    session = _session(lambda _m: UNRECEIPTED_STAT)
    events: list[tuple[str, dict]] = []

    run_turn(session, "wander", emit_callback=lambda name, payload: events.append((name, payload)))

    turn_updates = [p for (n, p) in events if n == "turn_update"]
    assert turn_updates, "expected a turn_update emit"
    assert any(v["rule_id"] == "R003" for v in turn_updates[0]["governance"])
