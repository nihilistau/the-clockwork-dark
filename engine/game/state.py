"""
Game State
==========

Canonical truth for all mechanical state.

Version: v0.1.0 [2026-06-20]
"""

from __future__ import annotations

import uuid
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Optional


class EvilPhase(str, Enum):
    """Background evil escalation phases."""

    DORMANT = "dormant"
    STIRRING = "stirring"
    SPREADING = "spreading"
    CONSUMING = "consuming"


@dataclass
class PlayerStats:
    """Player numeric stats."""

    hp: int = 20
    max_hp: int = 20
    stamina: int = 100
    focus: int = 10
    max_focus: int = 10
    craft: int = 10
    gold: int = 5


@dataclass
class InventoryItem:
    """Single inventory entry."""

    id: str
    name: str
    qty: int = 1
    tags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, "name": self.name, "qty": self.qty, "tags": list(self.tags)}


@dataclass
class AgentMind:
    """Agency knobs for Storyteller or Assistant."""

    intervention_willingness: float = 0.3
    cruelty_bias: float = 0.2
    reward_generosity: float = 0.5
    patience: float = 80.0
    trust_level: float = 20.0
    help_probability: float = 0.4
    current_form: str = "cat"
    appearance_schedule: str = "hidden"


@dataclass
class ProcgenResult:
    """Seeded world generation output (populated in PR7)."""

    seed: int = 0
    npcs: list[dict[str, Any]] = field(default_factory=list)
    buildings: list[dict[str, Any]] = field(default_factory=list)
    forest: dict[str, Any] = field(default_factory=dict)
    festival: dict[str, Any] = field(default_factory=dict)
    shrine_mural: str = ""
    bakery_job_day: int = 3

    def to_dict(self) -> dict[str, Any]:
        return {
            "seed": self.seed,
            "npcs": self.npcs,
            "buildings": self.buildings,
            "forest": self.forest,
            "festival": self.festival,
            "shrine_mural": self.shrine_mural,
            "bakery_job_day": self.bakery_job_day,
        }

    def npc_by_id(self, npc_id: str) -> Optional[dict[str, Any]]:
        """Return NPC dict by id."""
        for npc in self.npcs:
            if npc.get("id") == npc_id:
                return npc
        return None

    def npcs_at(self, location_id: str) -> list[dict[str, Any]]:
        """Return NPCs at a location."""
        return [n for n in self.npcs if n.get("location_id") == location_id]


@dataclass
class GameState:
    """Full session state."""

    session_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    player_name: str = "Traveler"
    archetype: str = "wayfarer"
    stats: PlayerStats = field(default_factory=PlayerStats)
    location_id: str = "forest_clearing"
    awareness: float = 0.0
    evil_phase: EvilPhase = EvilPhase.DORMANT
    evil_progress: float = 0.0
    plot_involvement: float = 0.0
    story_pressure: float = 0.0
    world_day: int = 1
    world_hour: int = 8
    inventory: list[InventoryItem] = field(default_factory=list)
    reputations: dict[str, int] = field(default_factory=dict)
    storyteller_mind: AgentMind = field(default_factory=AgentMind)
    assistant_mind: AgentMind = field(default_factory=AgentMind)
    procgen: ProcgenResult = field(default_factory=ProcgenResult)
    flags: dict[str, bool] = field(default_factory=dict)
    world_events: list[dict[str, Any]] = field(default_factory=list)
    rumors: list[str] = field(default_factory=list)
    last_sim_tick_at: float = 0.0
    media_cache: dict[str, str] = field(default_factory=dict)
    media_cutscenes_shown: list[str] = field(default_factory=list)
    last_cutscene_phase: str = ""
    turn_number: int = 0
    ended: bool = False
    save_version: int = 1

    def to_dict(self, *, include_hidden: bool = False) -> dict[str, Any]:
        """Serialize to dict. Redacts awareness unless include_hidden."""
        data: dict[str, Any] = {
            "session_id": self.session_id,
            "player_name": self.player_name,
            "archetype": self.archetype,
            "stats": asdict(self.stats),
            "location_id": self.location_id,
            "evil_phase": self.evil_phase.value,
            "plot_involvement": self.plot_involvement,
            "story_pressure": self.story_pressure,
            "world_day": self.world_day,
            "world_hour": self.world_hour,
            "inventory": [i.to_dict() for i in self.inventory],
            "reputations": dict(self.reputations),
            "flags": dict(self.flags),
            "world_events": list(self.world_events),
            "rumors": list(self.rumors),
            "last_sim_tick_at": self.last_sim_tick_at,
            "media_cache": dict(self.media_cache),
            "media_cutscenes_shown": list(self.media_cutscenes_shown),
            "last_cutscene_phase": self.last_cutscene_phase,
            "turn_number": self.turn_number,
            "ended": self.ended,
            "save_version": self.save_version,
            "procgen": self.procgen.to_dict(),
        }
        if include_hidden:
            data["awareness"] = self.awareness
            data["evil_progress"] = self.evil_progress
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> GameState:
        """Deserialize from dict."""
        stats_raw = data.get("stats", {})
        stats = PlayerStats(**stats_raw) if stats_raw else PlayerStats()
        inv = [
            InventoryItem(**item) if isinstance(item, dict) else item
            for item in data.get("inventory", [])
        ]
        procgen_raw = data.get("procgen", {})
        procgen = ProcgenResult(**procgen_raw) if procgen_raw else ProcgenResult()
        evil_progress = float(data.get("evil_progress", 0.0))
        # evil_progress is source of truth for phase on load
        from engine.game.evil_ticker import phase_from_progress

        phase = phase_from_progress(evil_progress)

        st_mind = data.get("storyteller_mind", {})
        as_mind = data.get("assistant_mind", {})

        return cls(
            session_id=data.get("session_id", uuid.uuid4().hex[:12]),
            player_name=data.get("player_name", "Traveler"),
            archetype=data.get("archetype", "wayfarer"),
            stats=stats,
            location_id=data.get("location_id", "forest_clearing"),
            awareness=float(data.get("awareness", 0.0)),
            evil_phase=phase,
            evil_progress=evil_progress,
            plot_involvement=float(data.get("plot_involvement", 0.0)),
            story_pressure=float(data.get("story_pressure", 0.0)),
            world_day=int(data.get("world_day", 1)),
            world_hour=int(data.get("world_hour", 8)),
            inventory=inv,
            reputations=dict(data.get("reputations", {})),
            storyteller_mind=AgentMind(**st_mind) if st_mind else AgentMind(),
            assistant_mind=AgentMind(**as_mind) if as_mind else AgentMind(),
            procgen=procgen,
            flags=dict(data.get("flags", {})),
            world_events=list(data.get("world_events", [])),
            rumors=list(data.get("rumors", [])),
            last_sim_tick_at=float(data.get("last_sim_tick_at", 0.0)),
            media_cache=dict(data.get("media_cache", {})),
            media_cutscenes_shown=list(data.get("media_cutscenes_shown", [])),
            last_cutscene_phase=str(data.get("last_cutscene_phase", "")),
            turn_number=int(data.get("turn_number", 0)),
            ended=bool(data.get("ended", False)),
            save_version=int(data.get("save_version", 1)),
        )