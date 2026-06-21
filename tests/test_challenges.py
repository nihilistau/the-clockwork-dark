"""Ephemeral structured challenges (PR29)."""

from __future__ import annotations

import json
import random

from engine.game.challenges import resolve_challenge, start_challenge
from engine.game.engine import GameEngine, set_active_engine
from engine.game.state import GameState
from engine.skills.registry import SKILL_REGISTRY
import engine.skills.builtin.mechanics  # noqa: F401


class _MaxRng(random.Random):
    def randint(self, a, b):  # type: ignore[override]
        return b


class _MinRng(random.Random):
    def randint(self, a, b):  # type: ignore[override]
        return a


def test_unknown_kind_errors():
    s = GameState()
    res = start_challenge(s, {"kind": "wat"})
    assert res.status == "error"
    assert s.challenge is None


def test_skill_gauntlet_success_applies_reward():
    s = GameState()
    spec = {
        "kind": "skill_gauntlet",
        "title": "Disarm the Cog-Harvester",
        "steps": [
            {"skill": "stealth", "dc": 12, "text": "Creep close."},
            {"skill": "craft", "dc": 14, "text": "Still the governor pin."},
        ],
        "reward": {"engagement": 10, "item": {"id": "brass_filings", "name": "Brass Filings"}},
        "fail": {"hp": -4},
    }
    start = start_challenge(s, spec)
    assert start.status == "active" and start.total_steps == 2
    r1 = resolve_challenge(s, rng=_MaxRng())  # step 1 passes
    assert r1.status == "active" and r1.step == 1
    r2 = resolve_challenge(s, rng=_MaxRng())  # step 2 passes -> success
    assert r2.status == "success" and r2.ended
    assert s.engagement == 10
    assert any(i.id == "brass_filings" for i in s.inventory)
    assert s.challenge is None


def test_skill_gauntlet_failure_applies_fail():
    s = GameState()
    s.stats.hp = 20
    spec = {"kind": "skill_gauntlet", "steps": [{"skill": "nerve", "dc": 18}], "fail": {"hp": -4}}
    start_challenge(s, spec)
    res = resolve_challenge(s, rng=_MinRng())  # fumble -> fail
    assert res.status == "failure" and res.ended
    assert s.stats.hp == 16
    assert s.challenge is None


def test_decision_tree_walks_to_terminal():
    s = GameState()
    spec = {
        "kind": "decision_tree",
        "start": "start",
        "nodes": {
            "start": {"text": "A fork.", "options": [
                {"id": "a", "text": "Left", "goto": "win"},
                {"id": "b", "text": "Right", "goto": "lose"}]},
            "win": {"terminal": True, "outcome": "success", "text": "Out.", "reward": {"awareness": 5}},
            "lose": {"terminal": True, "outcome": "failure", "text": "Lost.", "fail": {"stamina": -10}},
        },
    }
    start = start_challenge(s, spec)
    assert len(start.options) == 2
    res = resolve_challenge(s, choice="a")
    assert res.status == "success" and res.ended
    assert s.awareness == 5
    assert s.challenge is None


def test_puzzle_correct_and_attempts():
    s = GameState()
    spec = {"kind": "puzzle", "prompt": "The hour the mill stopped?", "answer": "III",
            "attempts": 2, "reward": {"engagement": 6}}
    start_challenge(s, spec)
    wrong = resolve_challenge(s, answer="iv")
    assert wrong.status == "active" and "1 attempts" in wrong.message
    right = resolve_challenge(s, answer="iii")  # normalized match
    assert right.status == "success"
    assert s.engagement == 6


def test_puzzle_exhausts_attempts():
    s = GameState()
    spec = {"kind": "puzzle", "answer": "x", "attempts": 1, "fail": {"hp": -2}}
    s.stats.hp = 10
    start_challenge(s, spec)
    res = resolve_challenge(s, answer="nope")
    assert res.status == "failure" and res.ended
    assert s.stats.hp == 8


def test_dice_table_resolves():
    s = GameState()
    spec = {"kind": "dice_table", "die": 6, "outcomes": [
        {"min": 1, "max": 6, "text": "A find.", "effect": {"item": {"id": "resin", "name": "Resin"}}}]}
    start_challenge(s, spec)
    res = resolve_challenge(s, rng=_MaxRng())
    assert res.status == "success"
    assert any(i.id == "resin" for i in s.inventory)


def test_challenge_persists_save_round_trip():
    s = GameState()
    start_challenge(s, {"kind": "puzzle", "answer": "k", "attempts": 3})
    restored = GameState.from_dict(s.to_dict())
    assert restored.challenge is not None
    assert restored.challenge["kind"] == "puzzle"


def test_challenge_skills_via_registry():
    s = GameState()
    eng = GameEngine(s)
    set_active_engine(eng)
    spec = {"kind": "skill_gauntlet", "steps": [{"skill": "craft", "dc": 5}], "reward": {"engagement": 4}}
    start = json.loads(SKILL_REGISTRY.invoke("start_challenge", spec=spec))
    assert start["status"] == "active"
    res = json.loads(SKILL_REGISTRY.invoke("resolve_challenge"))
    assert res["kind"] == "skill_gauntlet"
