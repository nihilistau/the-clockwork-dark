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