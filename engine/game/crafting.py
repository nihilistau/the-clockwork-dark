"""
Crafting & Professions (v0.2, PR14)
===================================

Engine-authoritative crafting. ``craft_item(recipe_id)`` checks the station,
verifies inputs, rolls a craft check (``d20 + stat//5 vs dc``), then consumes
inputs and grants the output. A natural 20 yields a *fine* extra; a fumble
spoils the materials. Recipes live in ``data/recipes/*.yaml``.

Version: v0.2.0 [2026-06-21]
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

import yaml

from engine.config import get_config
from engine.game.dice import roll_dice
from engine.game.state import GameState, InventoryItem

_ROOT = Path(__file__).resolve().parents[2]
_RECIPE_CACHE: Optional[dict[str, Any]] = None


def load_recipes() -> dict[str, Any]:
    """Load and cache every recipe from data/recipes/*.yaml (merged)."""
    global _RECIPE_CACHE
    if _RECIPE_CACHE is not None:
        return _RECIPE_CACHE
    rel = get_config().get("paths.recipes", "data/recipes")
    recipes_dir = _ROOT / rel
    merged: dict[str, Any] = {}
    if recipes_dir.is_dir():
        for path in sorted(recipes_dir.glob("*.yaml")):
            with path.open(encoding="utf-8") as fh:
                data = yaml.safe_load(fh) or {}
            merged.update(data)
    _RECIPE_CACHE = merged
    return _RECIPE_CACHE


def reset_recipe_cache() -> None:
    """Clear the recipe cache (tests only)."""
    global _RECIPE_CACHE
    _RECIPE_CACHE = None


@dataclass
class CraftResult:
    """Outcome of a crafting attempt."""

    recipe_id: str
    outcome: str  # crafted | failed | spoiled | missing_inputs | wrong_station | no_focus | unknown
    success: bool
    message: str
    output: Optional[dict[str, Any]] = None
    consumed: list[dict[str, Any]] = field(default_factory=list)
    quality: str = "normal"  # normal | fine (on a crit)
    craft_xp: int = 0
    dice: Optional[dict[str, Any]] = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "recipe_id": self.recipe_id,
            "outcome": self.outcome,
            "success": self.success,
            "message": self.message,
            "output": self.output,
            "consumed": self.consumed,
            "quality": self.quality,
            "craft_xp": self.craft_xp,
            "dice": self.dice,
        }


def list_recipes(state: Optional[GameState] = None) -> list[dict[str, Any]]:
    """Return recipe summaries, flagging which are craftable here & now."""
    recipes = load_recipes()
    out: list[dict[str, Any]] = []
    for rid, r in recipes.items():
        entry = {
            "id": rid,
            "name": r.get("name", rid),
            "station": r.get("station", "any"),
            "inputs": r.get("inputs", []),
            "output": r.get("output", {}),
        }
        if state is not None:
            entry["can_craft"] = _station_ok(state, r) and _has_inputs(state, r.get("inputs", []))
        out.append(entry)
    return out


def _station_ok(state: GameState, recipe: dict[str, Any]) -> bool:
    station = recipe.get("station", "any")
    return station in ("any", "", None) or state.location_id == station


def _find(state: GameState, item_id: str) -> Optional[InventoryItem]:
    return next((i for i in state.inventory if i.id == item_id), None)


def _has_inputs(state: GameState, inputs: list[dict[str, Any]]) -> bool:
    for inp in inputs:
        owned = _find(state, inp.get("id", ""))
        if owned is None or owned.qty < int(inp.get("qty", 1)):
            return False
    return True


def _missing_inputs(state: GameState, inputs: list[dict[str, Any]]) -> list[str]:
    missing = []
    for inp in inputs:
        owned = _find(state, inp.get("id", ""))
        if owned is None or owned.qty < int(inp.get("qty", 1)):
            missing.append(inp.get("id", ""))
    return missing


def _consume(state: GameState, inputs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    consumed = []
    for inp in inputs:
        owned = _find(state, inp.get("id", ""))
        qty = int(inp.get("qty", 1))
        if owned is not None:
            owned.qty -= qty
            consumed.append({"id": owned.id, "qty": qty})
            if owned.qty <= 0:
                state.inventory.remove(owned)
    return consumed


def _add_output(state: GameState, output: dict[str, Any], qty: int) -> None:
    oid = output.get("id", "")
    name = output.get("name", oid)
    if not oid:
        return
    existing = _find(state, oid)
    if existing is not None:
        existing.qty += qty
    else:
        state.inventory.append(InventoryItem(id=oid, name=name, qty=qty, tags=["crafted"]))


def craft_item(
    state: GameState,
    recipe_id: str,
    *,
    rng: Optional[random.Random] = None,
) -> CraftResult:
    """Attempt to craft ``recipe_id`` from the player's inventory."""
    recipes = load_recipes()
    recipe = recipes.get(recipe_id)
    if recipe is None:
        return CraftResult(recipe_id, "unknown", False, f"No such recipe: {recipe_id}.")

    if not _station_ok(state, recipe):
        station = recipe.get("station", "any")
        return CraftResult(
            recipe_id, "wrong_station", False,
            f"{recipe.get('name', recipe_id)} must be made at {station}.",
        )

    inputs = recipe.get("inputs", [])
    if not _has_inputs(state, inputs):
        missing = _missing_inputs(state, inputs)
        return CraftResult(
            recipe_id, "missing_inputs", False,
            f"You lack: {', '.join(missing)}.",
        )

    focus_cost = int(recipe.get("focus_cost", 0))
    if focus_cost and state.stats.focus < focus_cost:
        return CraftResult(recipe_id, "no_focus", False, "Not enough focus to attempt this.")

    skill_stat = recipe.get("skill", "craft")
    stat_val = state.stats.focus if skill_stat == "focus" else state.stats.craft
    dc = int(recipe.get("dc", 10))
    dice = roll_dice(20, modifier=stat_val // 5, reason=f"craft:{recipe_id}", rng=rng)

    if focus_cost:
        state.stats.focus = max(0, state.stats.focus - focus_cost)

    success = dice.critical or (not dice.fumble and dice.total >= dc)
    if not success:
        # A fumble spoils the materials; an ordinary miss leaves them intact.
        if dice.fumble:
            consumed = _consume(state, inputs)
            return CraftResult(
                recipe_id, "spoiled", False,
                f"The work goes wrong — your materials are ruined.",
                consumed=consumed, dice=dice.to_dict(),
            )
        return CraftResult(
            recipe_id, "failed", False,
            f"You can't quite manage the {recipe.get('name', recipe_id)} this time.",
            dice=dice.to_dict(),
        )

    consumed = _consume(state, inputs)
    output = dict(recipe.get("output", {}))
    qty = int(output.get("qty", 1))
    quality = "normal"
    if dice.critical:
        qty += 1
        quality = "fine"
    _add_output(state, output, qty)

    # Practice improves the craft stat (engine-owned progression).
    state.stats.craft = min(100, state.stats.craft + 1)
    hours = int(recipe.get("time_hours", 0))
    if hours:
        state.world_hour = (state.world_hour + hours) % 24

    name = output.get("name", output.get("id", recipe_id))
    msg = f"You craft {qty}× {name}."
    if quality == "fine":
        msg = f"A fine result — you craft {qty}× {name}."
    return CraftResult(
        recipe_id, "crafted", True, msg,
        output={"id": output.get("id", ""), "name": name, "qty": qty},
        consumed=consumed, quality=quality, craft_xp=1, dice=dice.to_dict(),
    )
