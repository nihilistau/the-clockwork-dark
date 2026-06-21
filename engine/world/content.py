"""
World Content Loader
====================

Loads synced world bible from data/world/content.yaml (from data.js).
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Optional

import yaml

from engine.config import get_config

logger = logging.getLogger(__name__)


def _phase_index(phase: str) -> int:
    from engine.game.evil_ticker import phase_index

    return phase_index(phase)

_ROOT = Path(__file__).resolve().parents[2]
_CONTENT_CACHE: Optional[dict[str, Any]] = None

_PHASE_ORDER = ("dormant", "stirring", "spreading", "consuming")


def _content_path() -> Path:
    rel = get_config().get("paths.world_content", "data/world/content.yaml")
    return _ROOT / rel


def reset_content_cache() -> None:
    """Clear cached content (tests)."""
    global _CONTENT_CACHE
    _CONTENT_CACHE = None


def load_world_content(*, force: bool = False) -> dict[str, Any]:
    """Load and cache world content YAML."""
    global _CONTENT_CACHE
    if _CONTENT_CACHE is not None and not force:
        return _CONTENT_CACHE

    path = _content_path()
    if not path.exists():
        logger.warning(
            "[world_content] Missing content file (operation=load, path=%s)", path
        )
        _CONTENT_CACHE = {}
        return _CONTENT_CACHE

    with path.open(encoding="utf-8") as fh:
        _CONTENT_CACHE = yaml.safe_load(fh) or {}
    return _CONTENT_CACHE


def get_place(location_id: str) -> dict[str, Any]:
    """Return place entry by id."""
    content = load_world_content()
    for place in content.get("places", []):
        if place.get("id") == location_id:
            return dict(place)
    return {}


def get_npc(npc_id: str) -> dict[str, Any]:
    """Return NPC entry by id."""
    content = load_world_content()
    for npc in content.get("npcs", []):
        if npc.get("id") == npc_id:
            return dict(npc)
    return {}


def all_npcs() -> list[dict[str, Any]]:
    """Return all canonical NPCs."""
    return list(load_world_content().get("npcs", []))


def all_places() -> list[dict[str, Any]]:
    """Return all canonical places."""
    return list(load_world_content().get("places", []))


def phase_meets_minimum(current: str, required: str) -> bool:
    """Return True if current evil phase >= required."""
    if not required or required == "dormant":
        return True
    try:
        return _phase_index(current) >= _phase_index(required)
    except KeyError:
        return True


def _gate_ok(
    evil_phase: str,
    min_phase: str,
    awareness: float,
    min_awareness: Optional[Any],
) -> bool:
    """A gate opens on phase OR awareness (March/Convergence arcs, DESIGN §1).

    ``min_awareness`` is an *alternative* unlock: e.g. the Marches open at
    evil >= SPREADING **or** Awareness >= 25, whichever comes first.
    """
    phase_ok = phase_meets_minimum(evil_phase, min_phase)
    if min_awareness is None:
        return phase_ok
    return phase_ok or awareness >= float(min_awareness)


def location_accessible(
    location_id: str,
    *,
    evil_phase: str,
    awareness: float = 0.0,
    discoveries: Optional[set[str]] = None,
) -> tuple[bool, str]:
    """
    Check phase/awareness and discovery gates for a location.

    Returns:
        (accessible, reason)
    """
    place = get_place(location_id)
    if not place and location_id not in _extra_location_ids():
        return False, f"Unknown location: {location_id}"

    min_phase = str(place.get("min_phase", "dormant"))
    min_awareness = place.get("min_awareness")
    if not _gate_ok(evil_phase, min_phase, awareness, min_awareness):
        if min_awareness is not None:
            return False, f"Locked until {min_phase} phase or awareness {min_awareness}"
        return False, f"Location locked until {min_phase} phase"

    if place.get("requires_discovery"):
        needed = "hidden_path"
        if discoveries is None or needed not in discoveries:
            return False, "Path not yet discovered"
    return True, "ok"


def _extra_location_ids() -> set[str]:
    """Event-only locations present in scene graph but not data.js places."""
    graph = load_world_content().get("scene_graph", {})
    place_ids = {p.get("id") for p in load_world_content().get("places", [])}
    return set(graph.keys()) - place_ids


def travel_edge_allowed(
    from_id: str,
    to_id: str,
    *,
    evil_phase: str,
    awareness: float = 0.0,
    discoveries: Optional[set[str]] = None,
) -> tuple[bool, str]:
    """Validate a travel edge including phase/awareness gates on the edge itself."""
    graph = load_world_content().get("scene_graph", {})
    edges = graph.get(from_id, [])
    edge = next((e for e in edges if e.get("to") == to_id), None)
    if edge is None:
        return False, f"No route from {from_id} to {to_id}"

    min_phase = str(edge.get("min_phase", "dormant"))
    min_awareness = edge.get("min_awareness")
    if not _gate_ok(evil_phase, min_phase, awareness, min_awareness):
        if min_awareness is not None:
            return False, f"Route locked until {min_phase} phase or awareness {min_awareness}"
        return False, f"Route locked until {min_phase} phase"

    req = edge.get("requires_discovery")
    if req and (discoveries is None or req not in discoveries):
        return False, f"Requires discovery: {req}"

    ok, reason = location_accessible(
        to_id, evil_phase=evil_phase, awareness=awareness, discoveries=discoveries
    )
    if not ok:
        return False, reason
    return True, "ok"


def rumors_for_phase(phase: str) -> list[str]:
    """Return rumor strings at or below the given phase."""
    content = load_world_content()
    idx = _phase_index(phase)
    out: list[str] = []
    for rumor in content.get("rumors", []):
        r_phase = str(rumor.get("phase", "dormant"))
        if _phase_index(r_phase) <= idx:
            text = rumor.get("text", "")
            if text:
                out.append(text)
    return out


def mural_fragment_for_phase(phase: str) -> str:
    """Return the latest mural fragment visible at phase."""
    content = load_world_content()
    idx = _phase_index(phase)
    fragment = ""
    for entry in content.get("mural", []):
        m_phase = str(entry.get("phase", "dormant"))
        if _phase_index(m_phase) <= idx:
            fragment = str(entry.get("frag", ""))
    return fragment


def cutscene_for_location(location_id: str) -> str:
    """Return cutscene id for a location visit, if mapped."""
    mapping = load_world_content().get("cutscene_map", {})
    return str(mapping.get(location_id, ""))


def overlay_for_location(location_id: str) -> str:
    """Return UI overlay key for location (trade, bakery, etc.)."""
    mapping = load_world_content().get("overlay_map", {})
    return str(mapping.get(location_id, ""))


def scene_graph_edges(from_id: str) -> list[dict[str, Any]]:
    """Return outbound travel edges for a location."""
    graph = load_world_content().get("scene_graph", {})
    return list(graph.get(from_id, []))


def location_metadata(location_id: str) -> dict[str, Any]:
    """Bundle place + overlay + cutscene for client."""
    place = get_place(location_id)
    return {
        "id": location_id,
        "name": place.get("name", location_id),
        "kind": place.get("kind", ""),
        "caption": place.get("caption", ""),
        "blurb": place.get("blurb", ""),
        "corrupted": bool(place.get("corrupted", False)),
        "overlay": overlay_for_location(location_id),
        "cutscene_id": cutscene_for_location(location_id),
        "min_phase": place.get("min_phase", "dormant"),
    }


def content_for_client() -> dict[str, Any]:
    """Serialize world content for the scene client."""
    content = load_world_content()
    return {
        "places": content.get("places", []),
        "npcs": content.get("npcs", []),
        "items": content.get("items", []),
        "bestiary": content.get("bestiary", []),
        "archetypes": content.get("archetypes", []),
        "assistant_forms": content.get("assistant_forms", []),
        "robes": content.get("robes", []),
        "rumors": content.get("rumors", []),
        "mural": content.get("mural", []),
        "weather": content.get("weather", []),
        "phases": content.get("phases", []),
        "overlay_map": content.get("overlay_map", {}),
        "cutscene_map": content.get("cutscene_map", {}),
    }