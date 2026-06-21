"""Assistant Director — the unreliable companion engine (PR27)."""

from __future__ import annotations

import random

from engine.agents.assistant import AssistantAgent, should_assistant_speak
from engine.agents.assistant_director import AssistantDirector
from engine.game.engine import GameEngine, set_active_engine
from engine.game.state import EvilPhase, GameState


class _LowRng(random.Random):
    def random(self) -> float:  # type: ignore[override]
        return 0.1


def test_calm_state_matches_legacy_gate():
    # In a calm default state the appear-roll equals should_assistant_speak.
    for hp in (0.0, 0.4, 1.0):
        s = GameState()
        s.assistant_mind.help_probability = hp
        d = AssistantDirector().decide(s, rng=random.Random(0))
        legacy = should_assistant_speak(hp, random.Random(0))
        assert d.appear == legacy


def test_indifferent_when_calm_and_low_help():
    s = GameState()
    s.assistant_mind.help_probability = 0.0
    d = AssistantDirector().decide(s, rng=_LowRng())
    assert d.appear is False
    assert d.intent == "silent"


def test_struggle_raises_score_and_intent():
    s = GameState()
    s.assistant_mind.help_probability = 0.0   # would be silent if calm
    s.stats.hp = 3                             # < 40% -> struggle 0.6
    d = AssistantDirector().decide(s, rng=_LowRng())
    assert d.appear is True
    assert d.intent in ("hint", "gift")
    assert d.score >= 0.5


def test_critical_hp_floor_makes_it_show():
    s = GameState()
    s.assistant_mind.help_probability = 0.0
    s.stats.hp = 2  # < 20% -> struggle 0.85 -> floor 0.9
    d = AssistantDirector().decide(s, rng=_LowRng())
    assert d.appear is True
    assert d.score >= 0.9


def test_gift_at_low_hp_with_trust():
    s = GameState()
    s.assistant_mind.help_probability = 1.0
    s.assistant_mind.trust_level = 50.0  # trust 0.5 >= 0.3
    s.stats.hp = 4
    d = AssistantDirector().decide(s, rng=_LowRng())  # gift roll 0.1 <= 0.5
    assert d.intent == "gift"
    assert d.gift_item["id"] == "bandage_poultice"


def test_low_trust_lowers_reliability():
    s = GameState()
    s.assistant_mind.help_probability = 1.0
    s.assistant_mind.trust_level = 0.0
    d = AssistantDirector().decide(s, rng=_LowRng())
    assert d.appear is True
    assert d.reliability < 0.5  # 0.45 + 0.5*0


def test_high_awareness_reflects_lore():
    s = GameState(awareness=50.0)
    s.assistant_mind.help_probability = 1.0
    d = AssistantDirector().decide(s, rng=_LowRng())
    assert d.intent == "lore"


def test_cooldown_after_recent_appearance():
    s = GameState()
    s.assistant_mind.help_probability = 0.5
    s.turn_number = 5
    s.flags["_assistant_last_turn"] = 4  # appeared 1 turn ago
    d = AssistantDirector().decide(s, rng=_LowRng())
    # score reduced by 0.3 cooldown (0.5 -> 0.2); 0.1 <= 0.2 still appears, but lower
    assert d.score <= 0.2 + 1e-9


def test_agent_executes_director_gift():
    s = GameState()
    s.assistant_mind.help_probability = 1.0
    s.assistant_mind.trust_level = 50.0
    s.stats.hp = 4
    eng = GameEngine(s)
    set_active_engine(eng)
    agent = AssistantAgent(eng, llm_fn=lambda _m: "Here — take this, you'll need it.", rng=_LowRng())
    res = agent.run_turn("the wolf circles, blood in the snow")
    assert res.intent == "gift"
    assert res.gift and res.gift["id"] == "bandage_poultice"
    assert any(i.id == "bandage_poultice" for i in s.inventory)
    assert any(r["skill"] == "assistant_gift" for r in res.tool_receipts)
