"""
World Effects — the Dark made tangible
======================================

The Doom Clock's *beats* (cog-harvesters in the wheat, the brass scarecrow
waking, clockwork-vines breaching the forest, the tunnels opening, the tower
assembling) used to fire only narration + a cutscene. Here they also **change
the world**, so the spread of the Clockwork Dark is something the player walks
into, not just reads about:

  * **flags** — durable world state the Storyteller and interceptors can read
    (``scarecrow_awake``, ``tunnels_open`` …).
  * **discoveries** — set ``discovery_<key>`` so gated edges/locations open. The
    tunnels opening literally unseals the road to Hollow Hill and the Mage-Ruins
    (see ``data/world/content.yaml`` ``requires_discovery``).
  * **rumors** — village chatter accrues, so the square/notice board reflect the
    spread.
  * **world_events** — a running ledger of what the Dark has done, kept coherent
    for narration.

All of this lands on *existing* ``GameState`` fields (flags / rumors /
world_events), so it serializes and round-trips with the save for free. Effects
are declarative and live in ``data/world/doom_effects.yaml``; applying a beat is
idempotent (callers gate on ``doom_beats_seen``, and each effect is a no-op when
already present).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

import yaml

from engine.config import get_config
from engine.game.state import GameState

_ROOT = Path(__file__).resolve().parents[2]
_CACHE: Optional[dict[str, Any]] = None


def load_doom_effects() -> dict[str, Any]:
    """Load + cache the beat -> world-effects table."""
    global _CACHE
    if _CACHE is not None:
        return _CACHE
    rel = get_config().get("paths.doom_effects", "data/world/doom_effects.yaml")
    path = _ROOT / rel
    if not path.exists():
        _CACHE = {}
        return _CACHE
    with path.open(encoding="utf-8") as fh:
        _CACHE = yaml.safe_load(fh) or {}
    return _CACHE


def reset_doom_effects_cache() -> None:
    global _CACHE
    _CACHE = None


def apply_beat_effects(state: GameState, beat_id: str) -> list[dict[str, str]]:
    """Apply the declarative world mutations for a crossed doom beat.

    Idempotent: setting a flag/discovery again is a no-op, rumors and
    world_events dedupe. Returns a list of ``{type, value}`` records applied
    (for telemetry / logging).
    """
    eff = load_doom_effects().get(beat_id)
    if not isinstance(eff, dict):
        return []
    applied: list[dict[str, str]] = []

    for flag in eff.get("set_flags", []) or []:
        if not state.flags.get(flag):
            applied.append({"type": "flag", "value": str(flag)})
        state.flags[flag] = True

    for key in eff.get("discoveries", []) or []:
        dkey = f"discovery_{key}"
        if not state.flags.get(dkey):
            applied.append({"type": "discovery", "value": str(key)})
        state.flags[dkey] = True

    for text in eff.get("rumors", []) or []:
        if text and text not in state.rumors:
            state.rumors.append(text)
            applied.append({"type": "rumor", "value": str(text)})

    seen_events = {(e.get("beat"), e.get("id")) for e in state.world_events}
    for ev in eff.get("world_events", []) or []:
        if not isinstance(ev, dict):
            continue
        key = (beat_id, ev.get("id"))
        if key in seen_events:
            continue
        state.world_events.append({**ev, "beat": beat_id})
        seen_events.add(key)
        applied.append({"type": "world_event", "value": str(ev.get("id", ""))})

    # NPCs move with the Dark: relocate named villagers as the world turns, so the
    # square fills and the margins empty (npcs_at reflects it for narration/UI).
    for npc_id, dest in (eff.get("npc_moves", {}) or {}).items():
        npc = state.procgen.npc_by_id(npc_id)
        if npc is None:
            npc = {"id": npc_id, "name": npc_id}
            state.procgen.npcs.append(npc)
        if npc.get("location_id") != dest:
            applied.append({"type": "npc_move", "value": f"{npc_id}->{dest}"})
        npc["location_id"] = str(dest)
        npc["displaced"] = True

    return applied
