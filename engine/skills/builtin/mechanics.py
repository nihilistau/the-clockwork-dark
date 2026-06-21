"""
Mechanics Skills
================

Required tools for Storyteller mechanical resolution.

Version: v0.1.0 [2026-06-20]
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from engine.config import get_config
from engine.game.engine import get_active_engine
from engine.skills.registry import TRIGGER_REQUIRED, skill

_ROOT = Path(__file__).resolve().parents[3]


def _load_economy() -> dict[str, Any]:
    path = get_config().get("paths.economy", "data/economy.yaml")
    economy_path = _ROOT / path
    if not economy_path.exists():
        return {}
    with economy_path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


@skill(
    pack="clockwork",
    description="Roll dice. MUST call before narrating any roll outcome.",
    category="GAME",
    trigger=TRIGGER_REQUIRED,
)
def roll_dice(sides: int = 20, modifier: int = 0, reason: str = "") -> str:
    """Roll dice via engine."""
    engine = get_active_engine()
    result = engine.roll(sides=sides, modifier=modifier, reason=reason)
    return json.dumps(result.to_dict())


@skill(
    pack="clockwork",
    description="Resolve d20 skill check vs DC. MUST call for risky actions.",
    category="GAME",
    trigger=TRIGGER_REQUIRED,
)
def resolve_skill_check(skill: str, dc: int, modifier: int = 0) -> str:
    """Skill check via engine."""
    engine = get_active_engine()
    return json.dumps(engine.skill_check(skill=skill, dc=dc, modifier=modifier))


@skill(
    pack="clockwork",
    description="Move player to location_id along the location graph.",
    category="GAME",
    trigger=TRIGGER_REQUIRED,
)
def move_to(location_id: str) -> str:
    """Travel via engine."""
    engine = get_active_engine()
    return json.dumps(engine.move_to(location_id).to_dict())


@skill(
    pack="clockwork",
    description="Browse, buy, or sell with an NPC vendor.",
    category="GAME",
    trigger="optional",
)
def trade(action: str, item_id: str = "", npc_id: str = "") -> str:
    """Trade using economy.yaml prices."""
    engine = get_active_engine()
    state = engine.state
    economy = _load_economy()
    vendor = economy.get(npc_id, {})

    if action == "browse":
        return json.dumps({"npc_id": npc_id, "sells": vendor.get("sells", {}), "buys": vendor.get("buys", {})})

    if action == "buy":
        sells = vendor.get("sells", {})
        item = sells.get(item_id)
        if not item:
            return json.dumps({"success": False, "message": f"{npc_id} does not sell {item_id}."})
        price = int(item.get("price", 0))
        if state.stats.gold < price:
            return json.dumps({"success": False, "message": "Not enough gold."})
        state.stats.gold -= price
        engine.add_item(item_id, item.get("name", item_id))
        rep_gain = int(vendor.get("reputation_per_buy", 0))
        if rep_gain:
            state.reputations[npc_id] = state.reputations.get(npc_id, 0) + rep_gain
        return json.dumps({
            "success": True,
            "item_id": item_id,
            "gold_spent": price,
            "gold": state.stats.gold,
            "reputation": state.reputations.get(npc_id, 0),
        })

    if action == "sell":
        buys = vendor.get("buys", {})
        item = buys.get(item_id)
        if not item:
            return json.dumps({"success": False, "message": f"{npc_id} does not buy {item_id}."})
        owned = next((i for i in state.inventory if i.id == item_id), None)
        if not owned or owned.qty < 1:
            return json.dumps({"success": False, "message": "You do not have that item."})
        price = int(item.get("price", 0))
        owned.qty -= 1
        if owned.qty <= 0:
            state.inventory.remove(owned)
        state.stats.gold += price
        return json.dumps({"success": True, "item_id": item_id, "gold_gained": price, "gold": state.stats.gold})

    return json.dumps({"success": False, "message": f"Unknown trade action: {action}"})


@skill(
    pack="clockwork",
    description="Advance world day and evil ticker (auto on tick).",
    category="SYSTEM",
    trigger="auto",
)
def advance_world_tick(days: float = 1.0, force_event: str = "") -> str:
    """World tick with optional forced schedule event (dev/test)."""
    engine = get_active_engine()
    force_events = [force_event] if force_event else None
    return json.dumps(engine.advance_world_day(days=days, force_events=force_events))


@skill(
    pack="clockwork",
    description="Storyteller-only: full evil and pressure snapshot.",
    category="NARRATIVE",
    trigger=TRIGGER_REQUIRED,
)
def query_evil_state() -> str:
    """Evil snapshot for GM narration."""
    engine = get_active_engine()
    return json.dumps(engine.get_evil_snapshot())


@skill(
    pack="clockwork",
    description=(
        "Register that the player meaningfully pushed back against the Clockwork "
        "Dark (investigated a harvester, cleared vines, sealed a seam, resisted). "
        "Raises engagement, which holds the Doom Clock back."
    ),
    category="GAME",
    trigger="optional",
)
def confront_darkness(intensity: int = 5) -> str:
    """Player engagement against the Dark (engine-authoritative)."""
    from engine.game.doom_clock import DoomClock

    engine = get_active_engine()
    amount = float(max(1, min(20, int(intensity))))
    value = DoomClock.register_engagement(engine.state, amount, "confront")
    return json.dumps({"success": True, "engagement": round(value, 1)})


@skill(
    pack="clockwork",
    description=(
        "Compose an ephemeral, engine-resolved challenge. Pass a 'spec' object with "
        "kind in {skill_gauntlet, decision_tree, puzzle, dice_table}. The engine "
        "validates the schema and adjudicates (rolls dice, walks the tree, checks the "
        "answer) — you supply structure, not the outcome."
    ),
    category="GAME",
    trigger="optional",
)
def start_challenge(spec: Any = None) -> str:
    """Begin an ephemeral structured challenge."""
    from engine.game.challenges import start_challenge as _start

    engine = get_active_engine()
    if isinstance(spec, str):
        try:
            spec = json.loads(spec)
        except Exception:
            spec = {}
    return json.dumps(_start(engine.state, spec or {}).to_dict())


@skill(
    pack="clockwork",
    description=(
        "Advance the active challenge: pass 'choice' (decision_tree) or 'answer' "
        "(puzzle); skill_gauntlet and dice_table just attempt/roll. Engine resolves."
    ),
    category="GAME",
    trigger="optional",
)
def resolve_challenge(choice: str = "", answer: str = "") -> str:
    """Advance the active challenge one step."""
    from engine.game.challenges import resolve_challenge as _resolve

    engine = get_active_engine()
    return json.dumps(_resolve(engine.state, choice=choice, answer=answer).to_dict())


@skill(
    pack="clockwork",
    description=(
        "Begin an authored set-piece challenge by id (e.g. 'tunnel_mouth') — a "
        "discoverable, engine-adjudicated encounter. Opens only once the world has "
        "reached it (flag/discovery gated, e.g. after the tunnels open). Then drive "
        "it with resolve_challenge like any challenge."
    ),
    category="GAME",
    trigger="optional",
)
def start_set_piece(set_piece_id: str = "") -> str:
    """Present an authored set-piece as an active challenge, if the world reached it."""
    from engine.game.set_pieces import start_set_piece as _start

    engine = get_active_engine()
    return json.dumps(_start(engine.state, set_piece_id).to_dict())


@skill(
    pack="clockwork",
    description=(
        "Resolve one combat action against a foe. MUST call before narrating any "
        "fight outcome. action in {attack, defend, flee, use_item, sympathy}; pass "
        "target_id (enemy id) to begin an encounter, item_id for use_item."
    ),
    category="GAME",
    trigger=TRIGGER_REQUIRED,
)
def resolve_combat(action: str, target_id: str = "", item_id: str = "") -> str:
    """Engine-authoritative combat resolution (v0.2)."""
    engine = get_active_engine()
    return json.dumps(engine.resolve_combat(action, target_id=target_id, item_id=item_id))


@skill(
    pack="clockwork",
    description="Return the active combat encounter snapshot (enemy hp, fear, round).",
    category="GAME",
    trigger=TRIGGER_REQUIRED,
)
def query_combat_state() -> str:
    """Current encounter snapshot for narration/UI."""
    engine = get_active_engine()
    return json.dumps(engine.combat_state())


@skill(
    pack="clockwork",
    description=(
        "Craft a recipe from the player's inventory (baking, herbalism, tinkering). "
        "Engine consumes inputs and grants the output. Pass recipe_id."
    ),
    category="GAME",
    trigger="optional",
)
def craft_item(recipe_id: str) -> str:
    """Crafting via engine (v0.2)."""
    engine = get_active_engine()
    return json.dumps(engine.craft_item(recipe_id))


@skill(
    pack="clockwork",
    description="List craftable recipes and whether each can be made here & now.",
    category="GAME",
    trigger="optional",
)
def list_recipes() -> str:
    """Recipe list for the crafting UI."""
    engine = get_active_engine()
    return json.dumps(engine.list_recipes())


@skill(
    pack="clockwork",
    description=(
        "Storyteller-only: snapshot of the Doom Clock convergence finale — whether the "
        "tower-era reckoning is open, its DC, which approach beats have fired, and any "
        "resolved outcome. Use to pace the endgame; it never advances evil itself."
    ),
    category="NARRATIVE",
    trigger="optional",
)
def query_convergence() -> str:
    """Convergence finale snapshot (approach beats + reckoning state)."""
    from engine.game.doom_clock import Convergence

    engine = get_active_engine()
    snap = Convergence.snapshot(engine.state)
    snap["pending_beats"] = [
        {"id": b.id, "text": b.text, "cutscene_id": b.cutscene_id}
        for b in Convergence.pending_reckoning_beats(engine.state)
    ]
    return json.dumps(snap)


@skill(
    pack="clockwork",
    description=(
        "Resolve the player's last engine-resolved choice at the clockwork tower. "
        "choice in {stand, unmake, walk_away}: 'walk_away' always succeeds (the quiet "
        "life carried to its end); 'stand'/'unmake' roll d20 + engagement vs the "
        "reckoning DC — success holds the line and ends the game un-consumed, failure "
        "leaves the clock to finish on its own. Only valid once convergence is open."
    ),
    category="GAME",
    trigger="optional",
)
def resolve_reckoning(choice: str) -> str:
    """Adjudicate the convergence finale's last choice (engine-authoritative)."""
    from engine.game.doom_clock import Convergence

    engine = get_active_engine()
    return json.dumps(Convergence.resolve_reckoning(engine.state, choice).to_dict())


@skill(
    pack="clockwork",
    description=(
        "List the clockwork foes a road ambush may name at the current evil phase, "
        "for narrating an arrival's 'something is on the road'. Read-only: the engine "
        "decides whether an ambush actually fired (it rides on move_to's result); this "
        "just tells you which foes are in play so you can describe them, then call "
        "resolve_combat(action='attack', target_id=<id>) if the player engages."
    ),
    category="NARRATIVE",
    trigger="optional",
)
def query_encounter_foes() -> str:
    """Clockwork foes an ambush may field at the player's current evil phase."""
    from engine.game.encounters import _enemy_name, _foes_for_phase
    from engine.game.evil_ticker import phase_index

    engine = get_active_engine()
    phase = engine.state.evil_phase.value
    foes = _foes_for_phase(phase_index(phase))
    return json.dumps({
        "evil_phase": phase,
        "foes": [{"id": fid, "name": _enemy_name(fid)} for fid in foes],
    })