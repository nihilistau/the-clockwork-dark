"""Inference resilience, turn budget, fallback, tool-failure propagation (PR18)."""

from __future__ import annotations

import pytest

from engine.agents.evaluator import StorytellerEvaluator
from engine.agents.resilience import (
    TurnBudget,
    approx_tokens,
    retry_call,
    with_retries,
)
from engine.game.engine import GameEngine, set_active_engine
from engine.game.state import GameState
from engine.agents.storyteller import StorytellerAgent


def test_approx_tokens():
    assert approx_tokens("") == 0
    assert approx_tokens("a" * 40) == 10


def test_turn_budget_tokens():
    b = TurnBudget(max_tokens=10)
    assert not b.exceeded()
    b.add_tokens(10)
    assert b.exceeded()
    assert "token budget" in b.reason()


def test_turn_budget_unlimited():
    b = TurnBudget()  # 0/0 = unlimited
    b.add_tokens(10_000)
    assert not b.exceeded()
    assert b.reason() == ""


def test_retry_call_succeeds_after_transient():
    calls = {"n": 0}

    def flaky():
        calls["n"] += 1
        if calls["n"] < 3:
            raise RuntimeError("transient")
        return "ok"

    out = retry_call(flaky, attempts=3, base_delay=0, sleep=lambda _s: None)
    assert out == "ok"
    assert calls["n"] == 3


def test_retry_call_raises_after_exhaustion():
    calls = {"n": 0}

    def always_fail():
        calls["n"] += 1
        raise ValueError("nope")

    with pytest.raises(ValueError):
        retry_call(always_fail, attempts=2, base_delay=0, sleep=lambda _s: None)
    assert calls["n"] == 2


def test_with_retries_decorator():
    state = {"n": 0}

    @with_retries(attempts=3, base_delay=0)
    def f():
        state["n"] += 1
        if state["n"] < 2:
            raise RuntimeError("x")
        return 42

    assert f() == 42
    assert state["n"] == 2


def test_storyteller_uses_configurable_fallback_on_failure():
    def raiser(_messages):
        raise RuntimeError("LM Studio down")

    eng = GameEngine(GameState())
    set_active_engine(eng)
    st = StorytellerAgent(eng, llm_fn=raiser)
    st._infer_backoff = 0.0  # don't sleep in tests
    res = st.run_turn("look around")
    assert res.narration == st._fallback_narration
    assert res.narration.startswith("The forest holds its breath")


def test_evaluator_flags_failed_required_tool():
    ev = StorytellerEvaluator()
    parsed = {"narration": "You swing and the wolf reels back into the mist.", "choices": [
        {"id": "a", "text": "Press"}, {"id": "b", "text": "Hold"}]}
    receipts = [{"skill": "resolve_combat", "success": False, "result": {"error": "no foe"}}]
    result = ev.evaluate(parsed["narration"], parsed, tool_receipts=receipts)
    assert any("failed" in n.lower() for n in result.notes)
    assert result.no_hallucinated_mechanics <= 0.4
    assert result.passed is False


def test_evaluator_ignores_failed_optional_tool():
    ev = StorytellerEvaluator()
    narration = (
        "The baker slides a warm loaf across the counter while the rain mutters "
        "against the shutters and the hearth crackles low and orange."
    )
    parsed = {"narration": narration, "choices": [
        {"id": "a", "text": "Thank her"}, {"id": "b", "text": "Leave"}]}
    receipts = [{"skill": "grant_hint", "success": False, "result": {"error": "x"}}]
    result = ev.evaluate(narration, parsed, tool_receipts=receipts)
    # optional tool failure is noted but does not hard-fail mechanics
    assert any("failed" in n.lower() for n in result.notes)
    assert result.no_hallucinated_mechanics == 1.0
