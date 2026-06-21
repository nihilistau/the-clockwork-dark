"""
Schedule Rolls
==============

Trader, tinker, and militia world events.

Version: v0.1.0 [2026-06-20]
"""

from __future__ import annotations

import logging
import random
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

import yaml

from engine.config import get_config
from engine.game.state import GameState

logger = logging.getLogger(__name__)

_ROOT = Path(__file__).resolve().parents[2]
_SCHEDULE_CACHE: Optional[dict[str, Any]] = None


@dataclass
class SimEvent:
    """World simulation event emitted on tick."""

    event_id: str
    day: int
    npc_ids: list[str] = field(default_factory=list)
    location_id: str = ""
    payload: dict[str, Any] = field(default_factory=dict)
    expires_day: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_id": self.event_id,
            "day": self.day,
            "npc_ids": list(self.npc_ids),
            "location_id": self.location_id,
            "payload": dict(self.payload),
            "expires_day": self.expires_day,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SimEvent:
        return cls(
            event_id=str(data.get("event_id", "")),
            day=int(data.get("day", 0)),
            npc_ids=list(data.get("npc_ids", [])),
            location_id=str(data.get("location_id", "")),
            payload=dict(data.get("payload", {})),
            expires_day=int(data.get("expires_day", 0)),
        )


def load_schedules() -> dict[str, Any]:
    """Load schedule config from YAML."""
    global _SCHEDULE_CACHE
    if _SCHEDULE_CACHE is not None:
        return _SCHEDULE_CACHE

    rel = get_config().get("paths.world_schedules", "data/world/schedules.yaml")
    path = _ROOT / rel
    if not path.exists():
        logger.warning(
            "[schedules] Config missing (operation=load_schedules, path=%s)", path
        )
        _SCHEDULE_CACHE = {}
        return _SCHEDULE_CACHE

    with path.open(encoding="utf-8") as fh:
        _SCHEDULE_CACHE = yaml.safe_load(fh) or {}
    return _SCHEDULE_CACHE


def _pick_rumor(rng: random.Random, schedules: dict[str, Any]) -> str:
    rumors = schedules.get("rumors", [])
    if not rumors:
        return "The village mutters, but nothing clear reaches you."
    return str(rng.choice(rumors))


def _event_active(state: GameState, event_id: str) -> bool:
    return any(e.get("event_id") == event_id for e in state.world_events)


class ScheduleRoll:
    """Roll trader/tinker/militia schedules against game state."""

    @staticmethod
    def check_caravan(
        state: GameState,
        rng: random.Random,
        *,
        schedules: Optional[dict[str, Any]] = None,
        force: bool = False,
    ) -> list[SimEvent]:
        """Roll caravan_arrival — 8% per day after day 5."""
        cfg = (schedules or load_schedules()).get("caravan_arrival", {})
        min_day = int(cfg.get("min_day", 5))
        if state.world_day < min_day:
            return []
        if _event_active(state, "caravan_arrival"):
            return []

        prob = float(cfg.get("probability_per_day", 0.08))
        if not force and rng.random() >= prob:
            return []

        rumor = _pick_rumor(rng, schedules or load_schedules())
        duration = int(cfg.get("duration_days", 2))
        npc_id = str(cfg.get("npc_id", "npc_odran"))
        location_id = str(cfg.get("location_id", "edgewood_square"))
        goods = list(cfg.get("goods", []))

        return [
            SimEvent(
                event_id="caravan_arrival",
                day=state.world_day,
                npc_ids=[npc_id],
                location_id=location_id,
                expires_day=state.world_day + duration,
                payload={"rumor": rumor, "goods": goods, "npc_id": npc_id},
            )
        ]

    @staticmethod
    def check_tinker(
        state: GameState,
        rng: random.Random,
        *,
        days_elapsed: float = 1.0,
        schedules: Optional[dict[str, Any]] = None,
        force: bool = False,
    ) -> list[SimEvent]:
        """Roll tinker_camp — 5% per week."""
        cfg = (schedules or load_schedules()).get("tinker_camp", {})
        if _event_active(state, "tinker_camp"):
            return []

        prob = float(cfg.get("probability_per_week", 0.05)) * (days_elapsed / 7.0)
        if not force and rng.random() >= prob:
            return []

        duration = int(cfg.get("duration_days", 3))
        npc_id = str(cfg.get("npc_id", "npc_ilya"))
        location_id = str(cfg.get("location_id", "tinker_caravan"))
        goods = list(cfg.get("goods", []))

        return [
            SimEvent(
                event_id="tinker_camp",
                day=state.world_day,
                npc_ids=[npc_id],
                location_id=location_id,
                expires_day=state.world_day + duration,
                payload={"goods": goods, "npc_id": npc_id},
            )
        ]

    @staticmethod
    def check_militia(
        state: GameState,
        rng: random.Random,
        *,
        schedules: Optional[dict[str, Any]] = None,
        force: bool = False,
    ) -> list[SimEvent]:
        """Roll militia_press — only if Awareness >= threshold."""
        cfg = (schedules or load_schedules()).get("militia_press", {})
        min_awareness = float(cfg.get("min_awareness", 20))
        if state.awareness < min_awareness:
            return []
        if _event_active(state, "militia_press"):
            return []

        prob = float(cfg.get("probability_per_day", 0.03))
        if not force and rng.random() >= prob:
            return []

        duration = int(cfg.get("duration_days", 1))
        npc_id = str(cfg.get("npc_id", "npc_sera"))
        location_id = str(cfg.get("location_id", "edgewood_square"))

        return [
            SimEvent(
                event_id="militia_press",
                day=state.world_day,
                npc_ids=[npc_id],
                location_id=location_id,
                expires_day=state.world_day + duration,
                payload={"npc_id": npc_id, "recruitment": True},
            )
        ]