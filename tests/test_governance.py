"""Governance pipeline + RulesGovernor wiring (PR19)."""

from __future__ import annotations

import pytest

from engine.governance import GovernancePipeline, TurnContext, get_governance, reset_governance
from engine.governance.governors import EvilPhaseTone, RulesGovernor, StorytellerMind
from engine.game.engine import GameEngine, set_active_engine
from engine.game.state import EvilPhase, GameState


@pytest.fixture(autouse=True)
def _reset():
    reset_governance()
    yield
    reset_governance()


def test_pipeline_runs_pre_in_priority_order():
    calls: list[str] = []

    class A:
        priority = 30
        name = "A"

        def run_pre(self, state, prompt, *, player_action="", **_):
            calls.append("A")
            return prompt + " A"

    class B:
        priority = 10
        name = "B"

        def run_pre(self, state, prompt, *, player_action="", **_):
            calls.append("B")
            return prompt + " B"

    pipe = GovernancePipeline(pre=[A(), B()])
    out = pipe.run_pre(GameState(), "base", player_action="x")
    assert calls == ["B", "A"]  # priority 10 before 30
    assert out == "base B A"


def test_from_config_builds_named_chains():
    pipe = get_governance()
    pre_names = [getattr(i, "name", "") for i in pipe.pre]
    post_names = [getattr(i, "name", "") for i in pipe.post]
    assert "LoreInjectInterceptor" in pre_names
    assert "AwarenessGateInterceptor" in pre_names
    assert "EvilPhaseTone" in pre_names
    assert "StorytellerMind" in pre_names
    assert "RulesGovernor" in post_names
    # AwarenessGate (40) must run after EvilPhaseTone (20) and StorytellerMind (30)
    assert pre_names.index("AwarenessGateInterceptor") > pre_names.index("EvilPhaseTone")


def test_evil_phase_tone_appends_line():
    s = GameState()
    s.evil_phase = EvilPhase.SPREADING
    out = EvilPhaseTone().run_pre(s, "PROMPT")
    assert "Tone:" in out and "dread" in out.lower()


def test_storyteller_mind_directive():
    s = GameState()
    s.storyteller_mind.cruelty_bias = 0.6
    s.storyteller_mind.reward_generosity = 0.7
    out = StorytellerMind().run_pre(s, "PROMPT")
    assert "GM disposition" in out
    assert "harsher" in out


def test_rules_governor_clamps_awareness_and_flags_r005():
    s = GameState()
    s.awareness = 150.0
    ctx = TurnContext(state=s, parsed={}, metadata={"evil_before": s.evil_progress})
    RulesGovernor().run_post(ctx)
    assert s.awareness == 100.0  # repaired
    assert any(v["rule_id"] == "R005" for v in ctx.violations)


def test_rules_governor_flags_evil_decrease_r004():
    s = GameState()
    s.evil_progress = 0.1
    ctx = TurnContext(state=s, parsed={}, metadata={"evil_before": 0.5})
    RulesGovernor().run_post(ctx)
    assert any(v["rule_id"] == "R004" for v in ctx.violations)


def test_rules_governor_flags_noncanonical_location_r001():
    s = GameState()
    s.location_id = "atlantis"
    ctx = TurnContext(state=s, parsed={}, metadata={"evil_before": s.evil_progress})
    RulesGovernor().run_post(ctx)
    assert any(v["rule_id"] == "R001" for v in ctx.violations)


def test_rules_governor_flags_unreceipted_stat_claim_r003():
    s = GameState()
    ctx = TurnContext(
        state=s,
        parsed={"stat_changes": {"hp": -5}},
        tool_receipts=[],  # no stat receipt
        metadata={"evil_before": s.evil_progress},
    )
    RulesGovernor().run_post(ctx)
    assert any(v["rule_id"] == "R003" for v in ctx.violations)


def test_storyteller_turn_records_governance_violations():
    raw = (
        '{"narration": "You feel the cold bite as your wound reopens in the mist, '
        'and the road blurs before your eyes for a moment.",'
        ' "choices": [{"id":"a","text":"Press on"},{"id":"b","text":"Rest"}],'
        ' "tool_calls": [], "stat_changes": {"hp": -4}}'
    )
    eng = GameEngine(GameState())
    set_active_engine(eng)
    from engine.agents.storyteller import StorytellerAgent

    st = StorytellerAgent(eng, llm_fn=lambda _m: raw)
    res = st.run_turn("wander into the cold")
    # the LLM claimed an hp delta with no roll/stat receipt -> R003 recorded
    assert any(v["rule_id"] == "R003" for v in res.governance)
