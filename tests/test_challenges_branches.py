"""Challenge branch + failure paths (gap closure).

Complements test_challenges.py with the resolver edges:
  * decision_tree: invalid-choice re-prompt (stays active), multi-hop
    traversal, and a losing terminal applying ``fail``;
  * skill_gauntlet: a later-step partial-fail (step 1 passes, step 2 fails);
  * dice_table: multi-bucket selection and the no-match fallback to
    ``outcomes[-1]``.
"""

from __future__ import annotations

import random

from engine.game.challenges import resolve_challenge, start_challenge
from engine.game.state import GameState


class _MaxRng(random.Random):
    def randint(self, a, b):  # type: ignore[override]
        return b


class _ScriptRng(random.Random):
    """Returns queued values from ``randint``, then sticks on the last."""

    def __init__(self, values):
        super().__init__()
        self._values = list(values)
        self._i = 0

    def randint(self, a, b):  # type: ignore[override]
        v = self._values[min(self._i, len(self._values) - 1)]
        self._i += 1
        return v


class _FixedRng(random.Random):
    def __init__(self, value):
        super().__init__()
        self._value = value

    def randint(self, a, b):  # type: ignore[override]
        return self._value


# --- decision_tree ----------------------------------------------------------

def test_decision_tree_invalid_choice_reprompts_and_stays_active():
    s = GameState()
    spec = {
        "kind": "decision_tree",
        "start": "start",
        "nodes": {
            "start": {"text": "A fork.", "options": [
                {"id": "a", "text": "Left", "goto": "win"}]},
            "win": {"terminal": True, "outcome": "success", "text": "Out.", "reward": {"awareness": 5}},
        },
    }
    start_challenge(s, spec)
    res = resolve_challenge(s, choice="zzz")  # not a valid option
    assert res.status == "active"
    assert res.message == "Pick one of the options."
    assert s.challenge is not None
    assert s.challenge["current"] == "start"  # did not advance
    assert s.awareness == 0.0  # no reward leaked


def test_decision_tree_multi_hop_to_losing_terminal_applies_fail():
    s = GameState()
    s.stats.stamina = 50
    spec = {
        "kind": "decision_tree",
        "start": "start",
        "nodes": {
            "start": {"text": "Mouth of the tunnel.", "options": [
                {"id": "in", "text": "Go in", "goto": "mid"}]},
            "mid": {"text": "A branching dark.", "options": [
                {"id": "left", "text": "Left", "goto": "dead_end"}]},
            "dead_end": {"terminal": True, "outcome": "failure", "text": "Caved in.",
                         "fail": {"stamina": -10}},
        },
    }
    start_challenge(s, spec)

    hop1 = resolve_challenge(s, choice="in")     # start -> mid (non-terminal)
    assert hop1.status == "active"
    assert s.challenge["current"] == "mid"
    assert "branching dark" in hop1.text

    hop2 = resolve_challenge(s, choice="left")   # mid -> dead_end (losing terminal)
    assert hop2.status == "failure" and hop2.ended
    assert hop2.success is False
    assert s.stats.stamina == 40  # fail effect applied
    assert s.challenge is None


# --- skill_gauntlet ---------------------------------------------------------

def test_skill_gauntlet_partial_fail_on_later_step():
    s = GameState()
    s.stats.hp = 20
    spec = {
        "kind": "skill_gauntlet",
        "title": "Cross the Tick-Field",
        "steps": [
            {"skill": "stealth", "dc": 10, "text": "Slip the first row."},
            {"skill": "nerve", "dc": 19, "text": "Hold as the scarecrow turns."},
        ],
        "reward": {"engagement": 10},
        "fail": {"hp": -5},
    }
    start = start_challenge(s, spec)
    assert start.total_steps == 2

    # roll 20 (pass step 1), then 1 (fumble -> fail step 2)
    rng = _ScriptRng([20, 1])
    r1 = resolve_challenge(s, rng=rng)
    assert r1.status == "active" and r1.step == 1  # advanced to step 2

    r2 = resolve_challenge(s, rng=rng)
    assert r2.status == "failure" and r2.ended
    assert r2.success is False
    assert s.stats.hp == 15           # fail effect applied
    assert s.engagement == 0.0        # reward NOT applied (didn't finish)
    assert s.challenge is None


# --- dice_table -------------------------------------------------------------

def test_dice_table_selects_matching_bucket():
    s = GameState()
    spec = {
        "kind": "dice_table",
        "die": 6,
        "outcomes": [
            {"min": 1, "max": 2, "text": "A scrap.", "effect": {"awareness": 1}},
            {"min": 3, "max": 4, "text": "A cog.", "effect": {"item": {"id": "cog", "name": "Cog"}}},
            {"min": 5, "max": 6, "text": "A windfall.", "effect": {"engagement": 5}},
        ],
    }
    start_challenge(s, spec)
    # roll lands a 3 -> the middle bucket
    res = resolve_challenge(s, rng=_FixedRng(3))
    assert res.status == "success"
    assert res.text == "A cog."
    assert any(i.id == "cog" for i in s.inventory)
    # only the matched bucket's effect applied
    assert s.engagement == 0.0
    assert s.awareness == 0.0


def test_dice_table_no_match_falls_back_to_last_outcome():
    s = GameState()
    spec = {
        "kind": "dice_table",
        "die": 6,
        "outcomes": [
            {"min": 1, "max": 2, "text": "Low.", "effect": {"awareness": 1}},
            {"min": 3, "max": 4, "text": "Fallback windfall.", "effect": {"engagement": 7}},
        ],
    }
    start_challenge(s, spec)
    # max roll on a d6 is 6, which matches no bucket -> falls back to outcomes[-1]
    res = resolve_challenge(s, rng=_MaxRng())
    assert res.status == "success"
    assert res.text == "Fallback windfall."
    assert s.engagement == 7
    assert s.awareness == 0.0
