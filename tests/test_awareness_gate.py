"""Awareness gate interceptor tests."""

from __future__ import annotations

from engine.lore.interceptors import AwarenessGateInterceptor, run_pre_interceptors
from engine.game.state import GameState


def test_strips_clockwork_dark_below_threshold():
    gate = AwarenessGateInterceptor()
    text = "The Clockwork Dark spreads through the wheat."
    result = gate.gate(text, awareness=10.0)
    assert "Clockwork Dark" not in result
    assert "something wrong in the wheat" in result


def test_preserves_term_above_threshold():
    gate = AwarenessGateInterceptor()
    text = "The Clockwork Dark spreads."
    result = gate.gate(text, awareness=25.0)
    assert "Clockwork Dark" in result


def test_run_pre_on_state():
    state = GameState(awareness=5.0)
    prompt = "Speak of the Clockwork Dark carefully."
    result = run_pre_interceptors(
        state,
        prompt,
        interceptors=[AwarenessGateInterceptor()],
    )
    assert "Clockwork Dark" not in result