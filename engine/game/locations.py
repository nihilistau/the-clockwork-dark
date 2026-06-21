"""
Location Graph
==============

Travel edges, evil multipliers, awareness deltas.
Synced from data/world/content.yaml scene_graph.

Version: v0.2.0 [2026-06-21]
"""

from __future__ import annotations

from typing import Any, Optional

from engine.world.content import load_world_content

# Ring and evil multiplier defaults for graph nodes
_LOCATION_META: dict[str, dict[str, Any]] = {
    "forest_clearing": {"name": "Forest Clearing", "ring": 0, "evil_multiplier": 0.5},
    "forest_forage": {"name": "Forest Margin", "ring": 0, "evil_multiplier": 0.55},
    "forest_vines": {"name": "Clockwork Vines", "ring": 0, "evil_multiplier": 0.7},
    "forest_poison": {"name": "Wrong Mist", "ring": 0, "evil_multiplier": 0.75},
    "resting_camp": {"name": "Roadside Camp", "ring": 0, "evil_multiplier": 0.5},
    "hurt_rest": {"name": "Wounded Rest", "ring": 0, "evil_multiplier": 0.45},
    "hollow_hill": {"name": "Hollow Hill", "ring": 0, "evil_multiplier": 0.65},
    "edgewood_square": {"name": "Edgewood Square", "ring": 1, "evil_multiplier": 0.8},
    "edgewood_bakery": {"name": "Edgewood Bakery", "ring": 1, "evil_multiplier": 0.7},
    "edgewood_forge": {"name": "The Forge", "ring": 1, "evil_multiplier": 0.8},
    "edgewood_shrine": {"name": "Shrine of Unnamed Saints", "ring": 1, "evil_multiplier": 0.75},
    "notice_board": {"name": "Notice Board", "ring": 1, "evil_multiplier": 0.8},
    "tinker_caravan": {"name": "Tinker Caravan", "ring": 1, "evil_multiplier": 0.9},
    "tinker_camp": {"name": "Tinker Camp", "ring": 1, "evil_multiplier": 0.85},
    "marches_road": {"name": "The Marches Road", "ring": 2, "evil_multiplier": 1.0},
    "wheatfield_warning": {"name": "Gear Drawing", "ring": 2, "evil_multiplier": 1.05},
    "scarecrow_field": {"name": "Wheatfield Scarecrow", "ring": 2, "evil_multiplier": 1.1},
    "millhaven_gate": {"name": "Millhaven Gate", "ring": 2, "evil_multiplier": 1.2},
    "corruption_border": {"name": "Corruption Border", "ring": 3, "evil_multiplier": 1.4},
    "ruins_temple": {"name": "Mage-Ruins", "ring": 2, "evil_multiplier": 1.15},
    "clockwork_tower": {"name": "Clockwork Tower", "ring": 3, "evil_multiplier": 1.6},
}


def _build_locations() -> dict[str, dict[str, Any]]:
    """Merge scene_graph edges with location metadata."""
    content = load_world_content()
    graph: dict[str, list[dict[str, Any]]] = content.get("scene_graph", {})
    locations: dict[str, dict[str, Any]] = {}

    for loc_id in set(graph.keys()) | set(_LOCATION_META.keys()):
        meta = dict(_LOCATION_META.get(loc_id, {"name": loc_id, "ring": 1, "evil_multiplier": 1.0}))
        place = next(
            (p for p in content.get("places", []) if p.get("id") == loc_id),
            {},
        )
        if place:
            meta["name"] = place.get("name", meta["name"])
            if place.get("corrupted"):
                meta["evil_multiplier"] = max(meta.get("evil_multiplier", 1.0), 1.1)

        connections: dict[str, dict[str, Any]] = {}
        for edge in graph.get(loc_id, []):
            to_id = str(edge.get("to", ""))
            if not to_id:
                continue
            connections[to_id] = {
                "hours": int(edge.get("hours", 1)),
                "danger_dc": int(edge.get("danger_dc", 10)),
                "awareness_delta": float(edge.get("awareness_delta", 0)),
                "min_phase": edge.get("min_phase"),
                "requires_discovery": edge.get("requires_discovery"),
            }
        meta["connections"] = connections
        locations[loc_id] = meta
    return locations


def get_locations() -> dict[str, dict[str, Any]]:
    """Return full location graph (rebuilt each call for test cache safety)."""
    return _build_locations()


# Module-level snapshot for CANONICAL_LOCATION_IDS
LOCATIONS: dict[str, dict[str, Any]] = get_locations()
CANONICAL_LOCATION_IDS = frozenset(LOCATIONS.keys())


def reload_locations() -> None:
    """Refresh LOCATIONS after content sync (tests)."""
    global LOCATIONS, CANONICAL_LOCATION_IDS
    LOCATIONS = get_locations()
    CANONICAL_LOCATION_IDS = frozenset(LOCATIONS.keys())


def get_location(location_id: str) -> Optional[dict[str, Any]]:
    """Return location metadata or None."""
    return get_locations().get(location_id)


def get_edge(from_id: str, to_id: str) -> Optional[dict[str, Any]]:
    """Return travel edge metadata if valid."""
    loc = get_location(from_id)
    if not loc:
        return None
    connections = loc.get("connections", {})
    return connections.get(to_id)


def can_travel(from_id: str, to_id: str) -> bool:
    """Return True if direct edge exists."""
    return get_edge(from_id, to_id) is not None


def evil_multiplier_for(location_id: str) -> float:
    """Return evil tick multiplier for location."""
    loc = get_location(location_id) or _LOCATION_META.get(location_id, {})
    return float(loc.get("evil_multiplier", 1.0))