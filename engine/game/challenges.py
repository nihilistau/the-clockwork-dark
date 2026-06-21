"""
Ephemeral Challenges (PR29)
===========================

Rigidly-structured, engine-resolved encounters the Storyteller can *compose*
mid-narration but cannot cheat. The AI supplies a declarative spec (validated
against a fixed schema); the engine owns resolution — rolling dice, walking the
tree, checking the answer. This is the "ephemeral tool call with rigid structure"
that lets the narrative AI improvise rule-bound dice gauntlets, decision trees,
and puzzles a deterministic engine adjudicates.

Kinds:
  * ``skill_gauntlet`` — an ordered sequence of d20 skill checks vs DCs.
  * ``decision_tree``  — branching nodes with options and terminal outcomes.
  * ``puzzle``         — a typed answer checked against the solution (N attempts).
  * ``dice_table``     — a weighted random outcome table.

The active challenge lives on ``GameState.challenge`` (persists across turns and
save/load); effects (engagement / item / hp / stamina / awareness) are applied
engine-authoritatively on resolution.

Version: v0.6.0 [2026-06-21]
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Any, Optional

from engine.game.dice import roll_dice
from engine.game.state import GameState, InventoryItem

KINDS = ("skill_gauntlet", "decision_tree", "puzzle", "dice_table")

# skill -> governing stat for the gauntlet modifier.
_SKILL_STAT = {
    "craft": "craft",
    "survival": "craft",
    "stealth": "focus",
    "persuasion": "focus",
    "sympathy": "focus",
    "lore": "focus",
    "nerve": "focus",
}


@dataclass
class ChallengeResult:
    challenge_id: str
    kind: str
    status: str  # active | success | failure | error
    text: str = ""
    options: list[dict[str, str]] = field(default_factory=list)
    answer_required: bool = False
    step: int = 0
    total_steps: int = 0
    dice: Optional[dict[str, Any]] = None
    effects: dict[str, Any] = field(default_factory=dict)
    message: str = ""
    ended: bool = False
    success: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "challenge_id": self.challenge_id,
            "kind": self.kind,
            "status": self.status,
            "text": self.text,
            "options": self.options,
            "answer_required": self.answer_required,
            "step": self.step,
            "total_steps": self.total_steps,
            "dice": self.dice,
            "effects": self.effects,
            "message": self.message,
            "ended": self.ended,
            "success": self.success,
        }


def _err(message: str, kind: str = "") -> ChallengeResult:
    return ChallengeResult("", kind, "error", message=message, ended=True)


def _norm(s: Any) -> str:
    return "".join(ch.lower() for ch in str(s) if ch.isalnum())


# --- lifecycle -----------------------------------------------------------

def start_challenge(
    state: GameState,
    spec: dict[str, Any],
    *,
    rng: Optional[random.Random] = None,
) -> ChallengeResult:
    """Validate a challenge spec and present its first step."""
    if not isinstance(spec, dict):
        return _err("Challenge spec must be an object.")
    kind = str(spec.get("kind", ""))
    if kind not in KINDS:
        return _err(f"Unknown challenge kind: {kind!r}.")
    cid = str(spec.get("id") or kind)
    title = str(spec.get("title", cid))

    if kind == "skill_gauntlet":
        steps = spec.get("steps")
        if not isinstance(steps, list) or not steps:
            return _err("skill_gauntlet needs a non-empty 'steps' list.", kind)
        state.challenge = {
            "id": cid, "kind": kind, "title": title,
            "steps": steps, "step": 0,
            "reward": spec.get("reward", {}), "fail": spec.get("fail", {}),
        }
        first = steps[0]
        return ChallengeResult(
            cid, kind, "active",
            text=str(first.get("text", "")), step=0, total_steps=len(steps),
            options=[{"id": "attempt", "text": "Attempt it"}],
            message=f"{title} — {first.get('skill','?')} DC {first.get('dc','?')}",
        )

    if kind == "decision_tree":
        nodes = spec.get("nodes")
        start = str(spec.get("start", "start"))
        if not isinstance(nodes, dict) or start not in nodes:
            return _err("decision_tree needs 'nodes' and a valid 'start'.", kind)
        state.challenge = {"id": cid, "kind": kind, "title": title, "nodes": nodes, "current": start}
        node = nodes[start]
        return ChallengeResult(
            cid, kind, "active",
            text=str(node.get("text", "")),
            options=[{"id": str(o.get("id")), "text": str(o.get("text", ""))}
                     for o in node.get("options", [])],
        )

    if kind == "puzzle":
        if "answer" not in spec:
            return _err("puzzle needs an 'answer'.", kind)
        attempts = int(spec.get("attempts", 3))
        state.challenge = {
            "id": cid, "kind": kind, "title": title,
            "answer": _norm(spec["answer"]), "attempts_left": attempts,
            "reward": spec.get("reward", {}), "fail": spec.get("fail", {}),
        }
        return ChallengeResult(
            cid, kind, "active", text=str(spec.get("prompt", title)),
            answer_required=True, message=f"{attempts} attempts",
        )

    # dice_table
    outcomes = spec.get("outcomes")
    if not isinstance(outcomes, list) or not outcomes:
        return _err("dice_table needs an 'outcomes' list.", kind)
    state.challenge = {
        "id": cid, "kind": kind, "title": title,
        "die": int(spec.get("die", 6)), "outcomes": outcomes,
    }
    return ChallengeResult(
        cid, kind, "active", text=str(spec.get("prompt", title)),
        options=[{"id": "roll", "text": "Roll"}],
    )


def resolve_challenge(
    state: GameState,
    *,
    choice: str = "",
    answer: str = "",
    rng: Optional[random.Random] = None,
) -> ChallengeResult:
    """Advance the active challenge by one step / choice / answer."""
    c = state.challenge
    if not c:
        return _err("No active challenge.")
    kind = c["kind"]
    if kind == "skill_gauntlet":
        return _resolve_gauntlet(state, c, rng)
    if kind == "decision_tree":
        return _resolve_tree(state, c, choice)
    if kind == "puzzle":
        return _resolve_puzzle(state, c, answer)
    return _resolve_dice_table(state, c, rng)


# --- resolvers -----------------------------------------------------------

def _resolve_gauntlet(state, c, rng) -> ChallengeResult:
    steps = c["steps"]
    idx = c["step"]
    step = steps[idx]
    skill = str(step.get("skill", "craft"))
    dc = int(step.get("dc", 12))
    stat = getattr(state.stats, _SKILL_STAT.get(skill, "craft"), 10)
    dice = roll_dice(20, modifier=stat // 5, reason=f"challenge:{skill}", rng=rng)
    success = dice.critical or (not dice.fumble and dice.total >= dc)
    cid, kind, title = c["id"], c["kind"], c["title"]

    if not success:
        effects = _apply_effects(state, c.get("fail", {}))
        state.challenge = None
        return ChallengeResult(
            cid, kind, "failure",
            text=str(step.get("on_fail_text", f"The {skill} check fails — {title} slips away.")),
            dice=dice.to_dict(), step=idx, total_steps=len(steps),
            effects=effects, ended=True, success=False,
        )

    idx += 1
    if idx >= len(steps):
        effects = _apply_effects(state, c.get("reward", {}))
        state.challenge = None
        return ChallengeResult(
            cid, kind, "success", text=f"{title} — done.",
            dice=dice.to_dict(), step=idx, total_steps=len(steps),
            effects=effects, ended=True, success=True,
        )

    c["step"] = idx
    nxt = steps[idx]
    return ChallengeResult(
        cid, kind, "active", text=str(nxt.get("text", "")),
        dice=dice.to_dict(), step=idx, total_steps=len(steps),
        options=[{"id": "attempt", "text": "Attempt it"}],
        message=f"{nxt.get('skill','?')} DC {nxt.get('dc','?')}",
    )


def _resolve_tree(state, c, choice) -> ChallengeResult:
    nodes = c["nodes"]
    node = nodes.get(c["current"], {})
    option = next((o for o in node.get("options", []) if str(o.get("id")) == choice), None)
    if option is None:
        return ChallengeResult(
            c["id"], c["kind"], "active", text=str(node.get("text", "")),
            options=[{"id": str(o.get("id")), "text": str(o.get("text", ""))}
                     for o in node.get("options", [])],
            message="Pick one of the options.",
        )
    target = nodes.get(str(option.get("goto", "")), {})
    if target.get("terminal"):
        outcome = str(target.get("outcome", "success"))
        effects = _apply_effects(state, target.get("reward" if outcome == "success" else "fail", {}))
        state.challenge = None
        return ChallengeResult(
            c["id"], c["kind"], outcome, text=str(target.get("text", "")),
            effects=effects, ended=True, success=(outcome == "success"),
        )
    c["current"] = str(option.get("goto"))
    return ChallengeResult(
        c["id"], c["kind"], "active", text=str(target.get("text", "")),
        options=[{"id": str(o.get("id")), "text": str(o.get("text", ""))}
                 for o in target.get("options", [])],
    )


def _resolve_puzzle(state, c, answer) -> ChallengeResult:
    if _norm(answer) == c["answer"]:
        effects = _apply_effects(state, c.get("reward", {}))
        state.challenge = None
        return ChallengeResult(
            c["id"], c["kind"], "success", text="The mechanism yields.",
            effects=effects, ended=True, success=True,
        )
    c["attempts_left"] = int(c["attempts_left"]) - 1
    if c["attempts_left"] <= 0:
        effects = _apply_effects(state, c.get("fail", {}))
        state.challenge = None
        return ChallengeResult(
            c["id"], c["kind"], "failure", text="The mechanism locks fast.",
            effects=effects, ended=True, success=False,
        )
    return ChallengeResult(
        c["id"], c["kind"], "active", text="Not quite — the dials reset.",
        answer_required=True, message=f"{c['attempts_left']} attempts left",
    )


def _resolve_dice_table(state, c, rng) -> ChallengeResult:
    dice = roll_dice(int(c.get("die", 6)), reason="challenge:table", rng=rng)
    roll = dice.total
    match = next(
        (o for o in c["outcomes"] if int(o.get("min", 1)) <= roll <= int(o.get("max", 99))),
        c["outcomes"][-1],
    )
    effects = _apply_effects(state, match.get("effect", {}))
    state.challenge = None
    return ChallengeResult(
        c["id"], c["kind"], "success", text=str(match.get("text", "")),
        dice=dice.to_dict(), effects=effects, ended=True, success=True,
    )


# --- effects (engine-authoritative) -------------------------------------

def _apply_effects(state: GameState, effects: dict[str, Any]) -> dict[str, Any]:
    applied: dict[str, Any] = {}
    if not isinstance(effects, dict):
        return applied
    if "engagement" in effects:
        from engine.game.doom_clock import DoomClock

        applied["engagement"] = DoomClock.register_engagement(state, float(effects["engagement"]))
    if "item" in effects and isinstance(effects["item"], dict):
        it = effects["item"]
        _add_item(state, str(it.get("id", "")), str(it.get("name", "")))
        applied["item"] = it
    if "hp" in effects:
        state.stats.hp = max(0, min(state.stats.max_hp, state.stats.hp + int(effects["hp"])))
        applied["hp"] = state.stats.hp
    if "stamina" in effects:
        state.stats.stamina = max(0, min(100, state.stats.stamina + int(effects["stamina"])))
        applied["stamina"] = state.stats.stamina
    if "awareness" in effects:
        state.awareness = max(0.0, min(100.0, state.awareness + float(effects["awareness"])))
        applied["awareness"] = state.awareness
    return applied


def _add_item(state: GameState, item_id: str, name: str) -> None:
    if not item_id:
        return
    for entry in state.inventory:
        if entry.id == item_id:
            entry.qty += 1
            return
    state.inventory.append(InventoryItem(id=item_id, name=name or item_id, qty=1, tags=["challenge"]))
