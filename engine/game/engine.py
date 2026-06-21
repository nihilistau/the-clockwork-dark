"""
Game Engine
===========

Action resolution — sole authority on state mutations.

Version: v0.1.0 [2026-06-20]
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

from engine.game.dice import DiceResult, resolve_check, roll_dice
from engine.game.evil_ticker import EvilTicker
from engine.game.locations import can_travel, get_edge, get_location, reload_locations
from engine.world.content import travel_edge_allowed
from engine.game.plot import PlotFormula
from engine.game.state import GameState, InventoryItem
from engine.world.world_sim import WorldSim


@dataclass
class MoveResult:
    """Travel outcome."""

    success: bool
    from_id: str
    to_id: str
    hours: int
    stamina_cost: int
    message: str
    awareness_delta: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "success": self.success,
            "from_id": self.from_id,
            "to_id": self.to_id,
            "hours": self.hours,
            "stamina_cost": self.stamina_cost,
            "message": self.message,
            "awareness_delta": self.awareness_delta,
        }


class GameEngine:
    """Deterministic game logic bound to a GameState."""

    def __init__(self, state: GameState) -> None:
        self.state = state

    @staticmethod
    def _discoveries(state: GameState) -> set[str]:
        """Return discovered path/location keys from flags."""
        found: set[str] = set()
        for key, value in state.flags.items():
            if not value:
                continue
            if key.startswith("discovery_"):
                found.add(key.replace("discovery_", "", 1))
            elif key == "hidden_path":
                found.add("hidden_path")
        return found

    def move_to(self, location_id: str) -> MoveResult:
        """Validate and execute travel along location graph."""
        reload_locations()
        current = self.state.location_id
        if location_id == current:
            return MoveResult(
                success=True,
                from_id=current,
                to_id=location_id,
                hours=0,
                stamina_cost=0,
                message="Already here.",
            )

        edge = get_edge(current, location_id)
        if edge is None:
            return MoveResult(
                success=False,
                from_id=current,
                to_id=location_id,
                hours=0,
                stamina_cost=0,
                message=f"Cannot travel from {current} to {location_id}.",
            )

        allowed, gate_reason = travel_edge_allowed(
            current,
            location_id,
            evil_phase=self.state.evil_phase.value,
            discoveries=self._discoveries(self.state),
        )
        if not allowed:
            return MoveResult(
                success=False,
                from_id=current,
                to_id=location_id,
                hours=0,
                stamina_cost=0,
                message=gate_reason,
            )

        hours = int(edge.get("hours", 1))
        stamina_cost = max(1, hours * 5)
        if self.state.stats.stamina < stamina_cost:
            return MoveResult(
                success=False,
                from_id=current,
                to_id=location_id,
                hours=hours,
                stamina_cost=stamina_cost,
                message="Not enough stamina.",
            )

        if get_location(location_id) is None:
            return MoveResult(
                success=False,
                from_id=current,
                to_id=location_id,
                hours=hours,
                stamina_cost=stamina_cost,
                message=f"Unknown location: {location_id}.",
            )

        self.state.stats.stamina -= stamina_cost
        self.state.location_id = location_id
        self.state.world_hour = (self.state.world_hour + hours) % 24
        if self.state.world_hour < hours:
            self.state.world_day += 1

        awareness_delta = float(edge.get("awareness_delta", 0))
        self.state.awareness = min(100.0, self.state.awareness + awareness_delta)
        PlotFormula.update_story_pressure(self.state)

        return MoveResult(
            success=True,
            from_id=current,
            to_id=location_id,
            hours=hours,
            stamina_cost=stamina_cost,
            message=f"Arrived at {location_id}.",
            awareness_delta=awareness_delta,
        )

    def roll(self, sides: int = 20, modifier: int = 0, reason: str = "") -> DiceResult:
        """Roll dice and attach to state audit log via flags."""
        result = roll_dice(sides=sides, modifier=modifier, reason=reason)
        self.state.flags["_last_dice"] = True
        return result

    def skill_check(self, skill: str, dc: int, modifier: int = 0) -> dict[str, Any]:
        """Roll d20 + modifier vs DC."""
        dice = self.roll(sides=20, modifier=modifier, reason=f"skill_check:{skill}")
        outcome = resolve_check(dice.total, dc)
        return {
            "skill": skill,
            "dice": dice.to_dict(),
            **outcome,
        }

    def advance_world_day(
        self,
        days: float = 1.0,
        *,
        force_events: Optional[list[str]] = None,
    ) -> dict[str, Any]:
        """Advance world time via WorldSim tick (evil, schedules, rumors)."""
        events = WorldSim.on_tick(
            self.state,
            days_elapsed=days,
            force=force_events,
        )
        return {
            "world_day": self.state.world_day,
            "evil_progress": self.state.evil_progress,
            "evil_phase": self.state.evil_phase.value,
            "plot_involvement": self.state.plot_involvement,
            "events": [e.to_dict() for e in events],
            "rumors": list(self.state.rumors),
        }

    def add_item(self, item_id: str, name: str, qty: int = 1) -> None:
        """Add or stack inventory item."""
        for entry in self.state.inventory:
            if entry.id == item_id:
                entry.qty += qty
                return
        self.state.inventory.append(
            InventoryItem(id=item_id, name=name, qty=qty, tags=[])
        )

    def get_evil_snapshot(self) -> dict[str, str | float]:
        """Storyteller-only evil state."""
        return EvilTicker.snapshot(self.state)

    def start_combat(self, enemy_id: str) -> dict[str, Any]:
        """Begin a grounded-combat encounter (v0.2)."""
        from engine.game.combat import start_combat

        return start_combat(self.state, enemy_id).to_dict()

    def resolve_combat(
        self, action: str, target_id: str = "", item_id: str = ""
    ) -> dict[str, Any]:
        """Resolve one combat action; engine owns all outcome math (v0.2)."""
        from engine.game.combat import resolve_combat

        return resolve_combat(
            self.state, action, target_id=target_id, item_id=item_id
        ).to_dict()

    def combat_state(self) -> dict[str, Any]:
        """Return the active encounter snapshot (v0.2)."""
        from engine.game.combat import combat_snapshot

        return combat_snapshot(self.state)

    def craft_item(self, recipe_id: str) -> dict[str, Any]:
        """Craft a recipe; engine owns the check and inventory math (v0.2)."""
        from engine.game.crafting import craft_item

        return craft_item(self.state, recipe_id).to_dict()

    def list_recipes(self) -> list[dict[str, Any]]:
        """Return recipe summaries, flagging which are craftable here & now."""
        from engine.game.crafting import list_recipes

        return list_recipes(self.state)


# Module-level engine for skill handlers (set per request in PR5+)
_active_engine: Optional[GameEngine] = None


def set_active_engine(engine: GameEngine) -> None:
    """Bind active engine for skill execution context."""
    global _active_engine
    _active_engine = engine


def get_active_engine() -> GameEngine:
    """Return active engine or raise."""
    if _active_engine is None:
        raise RuntimeError("No active GameEngine — call set_active_engine first")
    return _active_engine