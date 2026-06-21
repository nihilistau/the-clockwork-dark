"""
Chance Encounters on Travel (PR-more-world)
===========================================

Travel is calm by default — the quiet life is valid (see [[doom-arcs]]). But the
road is not *always* empty, and the deeper the Dark has spread, the less empty it
gets. When the player arrives somewhere, the engine rolls **once**, deterministic
and seedable, against the edge's ``danger_dc`` lifted by the current evil phase.

Three outcomes, in rising rarity:

  * ``none``      — nothing. The default; travel stays restful.
  * ``discovery`` — a small, harmless find: foraged goods, a scrap of lore, a coin
    in the road. Never combat, never a cost. Engine-granted reward.
  * ``ambush``    — something on the road. Names a ``clockwork``-tagged foe from the
    bestiary (escalating with the phase) that the *Storyteller* may start combat
    against via ``resolve_combat`` — the encounter only *offers* the fight, it never
    forces one. The engine never starts combat here; it stays advisory.

The roll is pure given (danger_dc, evil_phase, rng): pass a seeded ``random.Random``
and it is fully reproducible. With no danger (``danger_dc <= 0`` — town interiors,
zero-hour hops) it always returns ``none``.

Tunables live under config ``encounters:`` and in ``data/encounters.yaml`` (foe and
discovery tables by phase); both are optional — sane defaults are baked in so the
module works with neither file present, mirroring the combat/contracts pattern.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

import yaml

from engine.config import get_config
from engine.game.evil_ticker import phase_index
from engine.game.state import GameState

_ROOT = Path(__file__).resolve().parents[2]
_TABLE_CACHE: Optional[dict[str, Any]] = None

KIND_NONE = "none"
KIND_DISCOVERY = "discovery"
KIND_AMBUSH = "ambush"

# Baked-in fallbacks (used when config / data/encounters.yaml are absent).
# clockwork-tagged foes per phase index (0=dormant .. 3=consuming) — these ids
# must exist in data/bestiary.yaml and carry the "clockwork" tag.
_DEFAULT_FOES_BY_PHASE: dict[int, list[str]] = {
    0: ["scarecrow_brass"],
    1: ["scarecrow_brass"],
    2: ["scarecrow_brass", "clockwork_beast"],
    3: ["clockwork_beast", "husk"],
}

_DEFAULT_DISCOVERIES: list[dict[str, str]] = [
    {"id": "wild_herbs", "name": "Wild Herbs", "note": "A clump of yarrow and feverfew nods by the path."},
    {"id": "wild_mushroom", "name": "Wild Mushroom", "note": "A ring of pale caps, edible, half-hidden in moss."},
    {"id": "resin", "name": "Resin", "note": "Amber sap beads on a wounded birch — useful to a tinker."},
    {"id": "brass_filings", "name": "Brass Filings", "note": "Curls of brass glint in the ruts, swept from something that passed."},
    {"id": "old_clock_part", "name": "Old Clock Part", "note": "A toothed cog, half-buried, ticking faintly when you lift it."},
]


def _cfg() -> dict[str, Any]:
    """Encounter tunables (config ``encounters:`` over baked defaults)."""
    raw = get_config().get("encounters", {}) or {}
    return {
        "enabled": bool(raw.get("enabled", True)),
        # Base chance an encounter (of any kind) fires at all, before danger/phase.
        "base_chance": float(raw.get("base_chance", 0.18)),
        # How much each point of danger_dc above the floor adds to the chance.
        "danger_weight": float(raw.get("danger_weight", 0.02)),
        # Below this danger_dc the road is always calm (town hops, interiors).
        "danger_floor": int(raw.get("danger_floor", 8)),
        # Each evil phase index multiplies the chance (dormant..consuming).
        "phase_chance_mult": [
            float(x) for x in raw.get("phase_chance_mult", [0.5, 1.0, 1.4, 1.8])
        ],
        # Hard ceiling so travel never becomes a slog.
        "max_chance": float(raw.get("max_chance", 0.6)),
        # Of the encounters that fire, the share that are harmless discoveries.
        # The rest are ambushes. Discoveries dominate early; ambushes late.
        "discovery_share": [
            float(x) for x in raw.get("discovery_share", [0.85, 0.7, 0.5, 0.35])
        ],
    }


def load_encounter_tables() -> dict[str, Any]:
    """Load + cache optional ``data/encounters.yaml`` (foe / discovery tables)."""
    global _TABLE_CACHE
    if _TABLE_CACHE is not None:
        return _TABLE_CACHE
    rel = get_config().get("paths.encounters", "data/encounters.yaml")
    path = _ROOT / rel
    if not path.exists():
        _TABLE_CACHE = {}
        return _TABLE_CACHE
    with path.open(encoding="utf-8") as fh:
        _TABLE_CACHE = yaml.safe_load(fh) or {}
    return _TABLE_CACHE


def reset_encounter_cache() -> None:
    """Clear the encounter-table cache (tests / content sync)."""
    global _TABLE_CACHE
    _TABLE_CACHE = None


@dataclass
class Encounter:
    """A chance event computed on arrival. ``kind`` is none|discovery|ambush."""

    kind: str
    message: str = ""
    danger_dc: int = 0
    evil_phase: str = "dormant"
    # ambush-only:
    enemy_id: str = ""
    enemy_name: str = ""
    # discovery-only:
    reward: dict[str, Any] = field(default_factory=dict)
    # the 0..1 roll and the threshold it was tested against (audit/repro):
    roll: float = 0.0
    chance: float = 0.0

    @property
    def is_ambush(self) -> bool:
        return self.kind == KIND_AMBUSH

    @property
    def is_discovery(self) -> bool:
        return self.kind == KIND_DISCOVERY

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {
            "kind": self.kind,
            "message": self.message,
            "danger_dc": self.danger_dc,
            "evil_phase": self.evil_phase,
            "roll": round(self.roll, 4),
            "chance": round(self.chance, 4),
        }
        if self.kind == KIND_AMBUSH:
            data["enemy_id"] = self.enemy_id
            data["enemy_name"] = self.enemy_name
        elif self.kind == KIND_DISCOVERY:
            data["reward"] = dict(self.reward)
        return data


def _foes_for_phase(phase_idx: int) -> list[str]:
    tables = load_encounter_tables()
    by_phase = tables.get("foes_by_phase")
    if isinstance(by_phase, dict):
        # keys may be phase names or indices
        from engine.game.state import EvilPhase

        name = [EvilPhase.DORMANT, EvilPhase.STIRRING, EvilPhase.SPREADING, EvilPhase.CONSUMING][
            max(0, min(3, phase_idx))
        ].value
        foes = by_phase.get(name) or by_phase.get(phase_idx) or by_phase.get(str(phase_idx))
        if foes:
            return [str(f) for f in foes]
    return _DEFAULT_FOES_BY_PHASE.get(max(0, min(3, phase_idx)), ["scarecrow_brass"])


def _discoveries() -> list[dict[str, str]]:
    tables = load_encounter_tables()
    disc = tables.get("discoveries")
    if isinstance(disc, list) and disc:
        return [dict(d) for d in disc]
    return _DEFAULT_DISCOVERIES


def _enemy_name(enemy_id: str) -> str:
    """Look up a bestiary display name without forcing combat to load it."""
    try:
        from engine.game.combat import load_bestiary

        block = load_bestiary().get(enemy_id) or {}
        return str(block.get("name", enemy_id))
    except Exception:
        return enemy_id


def roll_encounter(
    danger_dc: int,
    evil_phase: str,
    *,
    rng: Optional[random.Random] = None,
) -> Encounter:
    """Pure, seedable encounter roll for an arrival.

    Args:
        danger_dc: the destination edge's danger_dc (higher = wilder road).
        evil_phase: current ``EvilPhase`` value (dormant..consuming).
        rng: optional seeded RNG; pass one for deterministic results.

    Returns:
        An :class:`Encounter` (``kind`` none|discovery|ambush).
    """
    cfg = _cfg()
    gen = rng or random
    phase_idx = phase_index(evil_phase)

    # Calm by default: no danger, no encounter. Town hops, interiors, disabled.
    if not cfg["enabled"] or danger_dc < cfg["danger_floor"]:
        return Encounter(kind=KIND_NONE, danger_dc=int(danger_dc), evil_phase=evil_phase)

    mults = cfg["phase_chance_mult"]
    phase_mult = mults[phase_idx] if phase_idx < len(mults) else mults[-1]
    over_floor = max(0, int(danger_dc) - cfg["danger_floor"])
    chance = (cfg["base_chance"] + over_floor * cfg["danger_weight"]) * phase_mult
    chance = max(0.0, min(cfg["max_chance"], chance))

    roll = gen.random()
    if roll >= chance:
        return Encounter(
            kind=KIND_NONE, danger_dc=int(danger_dc), evil_phase=evil_phase,
            roll=roll, chance=chance,
        )

    # An encounter fires — discovery or ambush?
    shares = cfg["discovery_share"]
    disc_share = shares[phase_idx] if phase_idx < len(shares) else shares[-1]
    kind_roll = gen.random()
    if kind_roll < disc_share:
        disc = _discoveries()
        pick = disc[gen.randrange(len(disc))] if disc else {"id": "", "name": "a small find"}
        note = str(pick.get("note", ""))
        name = str(pick.get("name", pick.get("id", "a small find")))
        msg = note or f"The road offers a small kindness: {name}."
        reward: dict[str, Any] = {}
        if pick.get("id"):
            reward = {"item": {"id": str(pick["id"]), "name": name}}
        return Encounter(
            kind=KIND_DISCOVERY, message=msg, danger_dc=int(danger_dc),
            evil_phase=evil_phase, reward=reward, roll=roll, chance=chance,
        )

    foes = _foes_for_phase(phase_idx)
    enemy_id = foes[gen.randrange(len(foes))] if foes else "scarecrow_brass"
    enemy_name = _enemy_name(enemy_id)
    msg = (
        f"Something is on the road that should not be — {enemy_name}, "
        "brass where bone should be, turning to face you."
    )
    return Encounter(
        kind=KIND_AMBUSH, message=msg, danger_dc=int(danger_dc), evil_phase=evil_phase,
        enemy_id=enemy_id, enemy_name=enemy_name, roll=roll, chance=chance,
    )


def grant_discovery(state: GameState, encounter: Encounter) -> dict[str, Any]:
    """Apply a discovery's small reward to state (engine-authoritative).

    Idempotent-ish: only grants for a discovery with a reward; ambush/none no-op.
    The Storyteller narrates; the engine grants. Returns the applied reward.
    """
    if encounter.kind != KIND_DISCOVERY or not encounter.reward:
        return {}
    item = encounter.reward.get("item")
    applied: dict[str, Any] = {}
    if isinstance(item, dict) and item.get("id"):
        _add_item(state, str(item["id"]), str(item.get("name", item["id"])))
        applied["item"] = dict(item)
    return applied


def _add_item(state: GameState, item_id: str, name: str, qty: int = 1) -> None:
    from engine.game.state import InventoryItem

    if not item_id:
        return
    for entry in state.inventory:
        if entry.id == item_id:
            entry.qty += qty
            return
    state.inventory.append(
        InventoryItem(id=item_id, name=name or item_id, qty=qty, tags=["found"])
    )
