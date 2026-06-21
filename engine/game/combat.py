"""
Grounded Combat (v0.2, PR13)
============================

Turn-based, engine-authoritative combat. The Storyteller narrates outcomes but
the numbers come from here — actions resolve as `d20 + mod vs enemy.defense`,
mirroring the skill-check engine. Fear and exhaustion erode the player's to-hit;
"sympathy" unmakes clockwork foes. The active encounter lives on
``GameState.combat`` so it persists across turns and save/load.

Actions: ``attack``, ``defend``, ``flee``, ``use_item``, ``sympathy``.

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
_BESTIARY_CACHE: Optional[dict[str, Any]] = None

# Item-effect keywords (matched against inventory item ids).
_HEAL_KEYS = ("bandage", "poultice", "herb", "loaf", "bread")
_NERVE_KEYS = ("talisman", "rune", "charm")
_STAMINA_KEYS = ("potion", "tonic")


def _combat_cfg() -> dict[str, Any]:
    cfg = get_config().get("combat", {}) or {}
    # Defaults mirror config/default.yaml so combat works even without it.
    return {
        "player_attack_mod": int(cfg.get("player_attack_mod", 2)),
        "player_base_defense": int(cfg.get("player_base_defense", 11)),
        "attack_die": int(cfg.get("attack_die", 6)),
        "defend_defense_bonus": int(cfg.get("defend_defense_bonus", 4)),
        "defend_stamina_regen": int(cfg.get("defend_stamina_regen", 6)),
        "flee_dc": int(cfg.get("flee_dc", 12)),
        "flee_stamina_cost": int(cfg.get("flee_stamina_cost", 8)),
        "fear_penalty_step": max(1, int(cfg.get("fear_penalty_step", 3))),
        "exhaustion_threshold": int(cfg.get("exhaustion_threshold", 25)),
        "exhaustion_penalty": int(cfg.get("exhaustion_penalty", 2)),
        "sympathy_focus_cost": int(cfg.get("sympathy_focus_cost", 3)),
        "sympathy_die": int(cfg.get("sympathy_die", 8)),
        "defeat_respawn_location": str(cfg.get("defeat_respawn_location", "edgewood_square")),
        "defeat_stamina_penalty": int(cfg.get("defeat_stamina_penalty", 40)),
    }


def load_bestiary() -> dict[str, Any]:
    """Load and cache enemy stat blocks from data/bestiary.yaml."""
    global _BESTIARY_CACHE
    if _BESTIARY_CACHE is not None:
        return _BESTIARY_CACHE
    rel = get_config().get("paths.bestiary", "data/bestiary.yaml")
    path = _ROOT / rel
    if not path.exists():
        _BESTIARY_CACHE = {}
        return _BESTIARY_CACHE
    with path.open(encoding="utf-8") as fh:
        _BESTIARY_CACHE = yaml.safe_load(fh) or {}
    return _BESTIARY_CACHE


def reset_bestiary_cache() -> None:
    """Clear the bestiary cache (tests only)."""
    global _BESTIARY_CACHE
    _BESTIARY_CACHE = None


@dataclass
class Enemy:
    """Mechanical enemy stat block."""

    id: str
    name: str
    hp: int
    defense: int
    to_hit: int
    damage: int
    fear: int = 1
    tags: list[str] = field(default_factory=list)
    loot: Optional[dict[str, str]] = None

    @classmethod
    def from_block(cls, enemy_id: str, block: dict[str, Any]) -> "Enemy":
        return cls(
            id=enemy_id,
            name=str(block.get("name", enemy_id)),
            hp=int(block.get("hp", 10)),
            defense=int(block.get("defense", 12)),
            to_hit=int(block.get("to_hit", 3)),
            damage=int(block.get("damage", 4)),
            fear=int(block.get("fear", 1)),
            tags=list(block.get("tags", [])),
            loot=block.get("loot"),
        )


@dataclass
class CombatResult:
    """Outcome of one combat action (one player action + enemy reaction)."""

    action: str
    outcome: str
    success: bool
    message: str
    enemy_id: str = ""
    enemy_name: str = ""
    enemy_hp: int = 0
    enemy_max_hp: int = 0
    player_hp: int = 0
    player_max_hp: int = 0
    player_stamina: int = 0
    focus: int = 0
    fear: int = 0
    round: int = 0
    damage_dealt: int = 0
    damage_taken: int = 0
    ended: bool = False
    victory: bool = False
    fled: bool = False
    defeat: bool = False
    loot: Optional[dict[str, str]] = None
    dice: Optional[dict[str, Any]] = None
    enemy_dice: Optional[dict[str, Any]] = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "action": self.action,
            "outcome": self.outcome,
            "success": self.success,
            "message": self.message,
            "enemy_id": self.enemy_id,
            "enemy_name": self.enemy_name,
            "enemy_hp": self.enemy_hp,
            "enemy_max_hp": self.enemy_max_hp,
            "player_hp": self.player_hp,
            "player_max_hp": self.player_max_hp,
            "player_stamina": self.player_stamina,
            "focus": self.focus,
            "fear": self.fear,
            "round": self.round,
            "damage_dealt": self.damage_dealt,
            "damage_taken": self.damage_taken,
            "ended": self.ended,
            "victory": self.victory,
            "fled": self.fled,
            "defeat": self.defeat,
            "loot": self.loot,
            "dice": self.dice,
            "enemy_dice": self.enemy_dice,
        }


_SUCCESS_OUTCOMES = {
    "engage", "hit", "defend", "item", "sympathy_unmake", "sympathy_calm",
    "victory", "fled",
}


def start_combat(
    state: GameState,
    enemy_id: str,
    *,
    rng: Optional[random.Random] = None,
) -> CombatResult:
    """Begin an encounter against ``enemy_id`` (ignored if one is active)."""
    bestiary = load_bestiary()
    block = bestiary.get(enemy_id)
    if block is None:
        return CombatResult(
            action="engage",
            outcome="error",
            success=False,
            message=f"No such foe: {enemy_id}.",
        )
    if state.combat is not None:
        return _snapshot_result("engage", "engage", True, "Already in combat.", state)

    enemy = Enemy.from_block(enemy_id, block)
    state.combat = {
        "enemy_id": enemy.id,
        "enemy_name": enemy.name,
        "enemy_hp": enemy.hp,
        "enemy_max_hp": enemy.hp,
        "enemy": block | {"id": enemy.id},
        "round": 0,
        "fear": 0,
        "defending": False,
    }
    return _snapshot_result(
        "engage", "engage", True, f"The {enemy.name} bars your way.", state
    )


def combat_snapshot(state: GameState) -> dict[str, Any]:
    """Return the current encounter state for UI/narration."""
    if state.combat is None:
        return {"active": False}
    c = state.combat
    return {
        "active": True,
        "enemy_id": c["enemy_id"],
        "enemy_name": c["enemy_name"],
        "enemy_hp": c["enemy_hp"],
        "enemy_max_hp": c["enemy_max_hp"],
        "round": c.get("round", 0),
        "fear": c.get("fear", 0),
        "player_hp": state.stats.hp,
        "player_max_hp": state.stats.max_hp,
        "player_stamina": state.stats.stamina,
        "focus": state.stats.focus,
    }


def resolve_combat(
    state: GameState,
    action: str,
    target_id: str = "",
    item_id: str = "",
    *,
    rng: Optional[random.Random] = None,
) -> CombatResult:
    """Resolve one combat action; starts an encounter if ``target_id`` given."""
    cfg = _combat_cfg()

    if state.combat is None:
        if not target_id:
            return CombatResult(
                action=action,
                outcome="error",
                success=False,
                message="No active combat and no target specified.",
            )
        started = start_combat(state, target_id, rng=rng)
        if not started.success:
            return started

    combat = state.combat
    assert combat is not None
    enemy = Enemy.from_block(combat["enemy"]["id"], combat["enemy"])
    combat["round"] = int(combat.get("round", 0)) + 1
    combat["defending"] = False
    stats = state.stats

    penalty = combat.get("fear", 0) // cfg["fear_penalty_step"]
    if stats.stamina < cfg["exhaustion_threshold"]:
        penalty += cfg["exhaustion_penalty"]

    dice_dict: Optional[dict[str, Any]] = None
    damage_dealt = 0
    outcome = ""
    message = ""

    if action == "attack":
        dice = roll_dice(20, modifier=cfg["player_attack_mod"] - penalty, reason="attack", rng=rng)
        dice_dict = dice.to_dict()
        if dice.critical or (not dice.fumble and dice.total >= enemy.defense):
            dmg = roll_dice(cfg["attack_die"], reason="damage", rng=rng).total
            if dice.critical:
                dmg *= 2
            combat["enemy_hp"] = max(0, combat["enemy_hp"] - dmg)
            damage_dealt = dmg
            outcome, message = "hit", f"You strike the {enemy.name} for {dmg}."
        else:
            outcome, message = "miss", f"Your blow glances off the {enemy.name}."

    elif action == "defend":
        combat["defending"] = True
        stats.stamina = min(100, stats.stamina + cfg["defend_stamina_regen"])
        outcome, message = "defend", "You set your guard and steady your breath."

    elif action == "flee":
        dice = roll_dice(20, reason="flee", rng=rng)
        dice_dict = dice.to_dict()
        stats.stamina = max(0, stats.stamina - cfg["flee_stamina_cost"])
        if dice.total >= cfg["flee_dc"]:
            return _finish(state, "fled", f"You break away from the {enemy.name}.",
                           action="flee", dice=dice_dict, fled=True)
        outcome, message = "flee_failed", f"You stumble — the {enemy.name} is still on you."

    elif action == "use_item":
        ok, message = _apply_item(state, item_id, combat)
        outcome = "item" if ok else "item_failed"

    elif action == "sympathy":
        outcome, message, damage_dealt, dice_dict = _resolve_sympathy(
            state, combat, enemy, cfg, rng
        )

    else:
        return _snapshot_result(
            action, "error", False, f"Unknown combat action: {action}.", state
        )

    # Victory before the enemy can react.
    if combat["enemy_hp"] <= 0:
        return _finish(state, "victory", f"The {enemy.name} falls still.",
                       action=action, dice=dice_dict, damage_dealt=damage_dealt,
                       victory=True, loot=enemy.loot)

    # Enemy reaction (using an item / failing to flee still costs you the round).
    enemy_dice_dict, damage_taken, enemy_msg = _enemy_attack(state, combat, enemy, cfg, rng)

    if stats.hp <= 0:
        return _finish(state, "defeat", "The world tilts and goes dark.",
                       action=action, dice=dice_dict, enemy_dice=enemy_dice_dict,
                       damage_dealt=damage_dealt, damage_taken=damage_taken, defeat=True)

    state.combat = combat
    full_msg = message + ((" " + enemy_msg) if enemy_msg else "")
    return CombatResult(
        action=action,
        outcome=outcome,
        success=outcome in _SUCCESS_OUTCOMES,
        message=full_msg.strip(),
        enemy_id=enemy.id,
        enemy_name=enemy.name,
        enemy_hp=combat["enemy_hp"],
        enemy_max_hp=combat["enemy_max_hp"],
        player_hp=stats.hp,
        player_max_hp=stats.max_hp,
        player_stamina=stats.stamina,
        focus=stats.focus,
        fear=combat.get("fear", 0),
        round=combat["round"],
        damage_dealt=damage_dealt,
        damage_taken=damage_taken,
        dice=dice_dict,
        enemy_dice=enemy_dice_dict,
    )


def _resolve_sympathy(
    state: GameState,
    combat: dict[str, Any],
    enemy: Enemy,
    cfg: dict[str, Any],
    rng: Optional[random.Random],
) -> tuple[str, str, int, Optional[dict[str, Any]]]:
    """Focus-fuelled sympathy: unmakes clockwork foes, calms others."""
    if state.stats.focus < cfg["sympathy_focus_cost"]:
        return "sympathy_failed", "Not enough focus to reach for sympathy.", 0, None
    state.stats.focus -= cfg["sympathy_focus_cost"]
    dice = roll_dice(20, modifier=max(0, state.stats.focus // 2), reason="sympathy", rng=rng)
    if dice.fumble or (not dice.critical and dice.total < enemy.defense):
        return "sympathy_miss", "The sympathy slips from your grasp.", 0, dice.to_dict()
    if "clockwork" in enemy.tags:
        dmg = roll_dice(cfg["sympathy_die"], reason="unmaking", rng=rng).total
        combat["enemy_hp"] = max(0, combat["enemy_hp"] - dmg)
        return ("sympathy_unmake",
                f"You name the {enemy.name}'s making; its gears loosen for {dmg}.",
                dmg, dice.to_dict())
    combat["enemy"]["to_hit"] = max(0, int(combat["enemy"].get("to_hit", enemy.to_hit)) - 1)
    return ("sympathy_calm",
            f"You speak the old calming names; the {enemy.name} falters.",
            0, dice.to_dict())


def _enemy_attack(
    state: GameState,
    combat: dict[str, Any],
    enemy: Enemy,
    cfg: dict[str, Any],
    rng: Optional[random.Random],
) -> tuple[Optional[dict[str, Any]], int, str]:
    """Enemy strikes back; returns (dice, damage_taken, message)."""
    to_hit = int(combat["enemy"].get("to_hit", enemy.to_hit))  # sympathy may have lowered it
    defense = cfg["player_base_defense"] + (cfg["defend_defense_bonus"] if combat["defending"] else 0)
    dice = roll_dice(20, modifier=to_hit, reason="enemy_attack", rng=rng)
    if dice.critical or (not dice.fumble and dice.total >= defense):
        dmg = enemy.damage
        if combat["defending"]:
            dmg = max(1, dmg - 2)
        state.stats.hp = max(0, state.stats.hp - dmg)
        combat["fear"] = min(10, combat.get("fear", 0) + enemy.fear)
        return dice.to_dict(), dmg, f"The {enemy.name} lands a blow for {dmg}."
    return dice.to_dict(), 0, f"The {enemy.name}'s attack misses."


def _apply_item(state: GameState, item_id: str, combat: dict[str, Any]) -> tuple[bool, str]:
    """Use an inventory item in combat (heal / steady nerve / restore stamina)."""
    item = None
    if item_id:
        item = next((i for i in state.inventory if i.id == item_id), None)
    if item is None:
        item = next(
            (i for i in state.inventory
             if any(k in i.id for k in _HEAL_KEYS + _NERVE_KEYS + _STAMINA_KEYS)),
            None,
        )
    if item is None or item.qty < 1:
        return False, "You have no usable item."

    iid = item.id
    if any(k in iid for k in _HEAL_KEYS):
        heal = 8
        state.stats.hp = min(state.stats.max_hp, state.stats.hp + heal)
        msg = f"You use {item.name}; +{heal} HP."
    elif any(k in iid for k in _NERVE_KEYS):
        combat["fear"] = 0
        msg = f"{item.name} steadies your nerve; fear fades."
    elif any(k in iid for k in _STAMINA_KEYS):
        state.stats.stamina = min(100, state.stats.stamina + 30)
        msg = f"You drink {item.name}; stamina returns."
    else:
        return False, f"{item.name} does nothing in a fight."

    item.qty -= 1
    if item.qty <= 0:
        state.inventory.remove(item)
    return True, msg


def _finish(
    state: GameState,
    outcome: str,
    message: str,
    *,
    action: str,
    dice: Optional[dict[str, Any]] = None,
    enemy_dice: Optional[dict[str, Any]] = None,
    damage_dealt: int = 0,
    damage_taken: int = 0,
    victory: bool = False,
    fled: bool = False,
    defeat: bool = False,
    loot: Optional[dict[str, str]] = None,
) -> CombatResult:
    """End the encounter, apply victory loot / defeat respawn, clear state.combat."""
    combat = state.combat or {}
    enemy_id = combat.get("enemy_id", "")
    enemy_name = combat.get("enemy_name", "")
    enemy_max = combat.get("enemy_max_hp", 0)
    enemy_hp = combat.get("enemy_hp", 0)
    fear = combat.get("fear", 0)
    rnd = combat.get("round", 0)

    if victory and loot:
        _add_item(state, loot.get("id", ""), loot.get("name", ""))
    if victory and "clockwork" in (combat.get("enemy", {}) or {}).get("tags", []):
        # Beating back the Dark holds it: raise engagement (slows the Doom Clock).
        from engine.game.doom_clock import DoomClock

        DoomClock.register_engagement(state, 8.0, "defeated clockwork foe")
    if defeat:
        cfg = _combat_cfg()
        state.location_id = cfg["defeat_respawn_location"]
        state.stats.hp = max(1, state.stats.max_hp // 2)
        state.stats.stamina = max(0, state.stats.stamina - cfg["defeat_stamina_penalty"])
        state.flags["combat_defeat"] = True

    state.combat = None
    return CombatResult(
        action=action,
        outcome=outcome,
        success=outcome in _SUCCESS_OUTCOMES,
        message=message,
        enemy_id=enemy_id,
        enemy_name=enemy_name,
        enemy_hp=enemy_hp,
        enemy_max_hp=enemy_max,
        player_hp=state.stats.hp,
        player_max_hp=state.stats.max_hp,
        player_stamina=state.stats.stamina,
        focus=state.stats.focus,
        fear=fear,
        round=rnd,
        damage_dealt=damage_dealt,
        damage_taken=damage_taken,
        ended=True,
        victory=victory,
        fled=fled,
        defeat=defeat,
        loot=loot if victory else None,
        dice=dice,
        enemy_dice=enemy_dice,
    )


def _snapshot_result(
    action: str, outcome: str, success: bool, message: str, state: GameState
) -> CombatResult:
    snap = combat_snapshot(state)
    return CombatResult(
        action=action,
        outcome=outcome,
        success=success,
        message=message,
        enemy_id=snap.get("enemy_id", ""),
        enemy_name=snap.get("enemy_name", ""),
        enemy_hp=snap.get("enemy_hp", 0),
        enemy_max_hp=snap.get("enemy_max_hp", 0),
        player_hp=state.stats.hp,
        player_max_hp=state.stats.max_hp,
        player_stamina=state.stats.stamina,
        focus=state.stats.focus,
        fear=snap.get("fear", 0),
        round=snap.get("round", 0),
    )


def _add_item(state: GameState, item_id: str, name: str, qty: int = 1) -> None:
    if not item_id:
        return
    for entry in state.inventory:
        if entry.id == item_id:
            entry.qty += qty
            return
    state.inventory.append(InventoryItem(id=item_id, name=name or item_id, qty=qty, tags=[]))
