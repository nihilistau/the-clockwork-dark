"""
Procgen — seeded Edgewood village and forest margin.

Version: v0.1.0 [2026-06-20]
"""

from __future__ import annotations

import logging
import random
import secrets
from pathlib import Path
from typing import Any, Optional

import yaml

from engine.config import get_config
from engine.game.state import GameState, ProcgenResult

logger = logging.getLogger(__name__)

_ROOT = Path(__file__).resolve().parents[2]
_TEMPLATE_CACHE: Optional[dict[str, Any]] = None


def _templates_path() -> Path:
    rel = get_config().get(
        "paths.procgen_templates",
        "data/procgen_templates/edgewood.yaml",
    )
    return _ROOT / rel


def load_templates() -> dict[str, Any]:
    """Load and cache Edgewood procgen templates."""
    global _TEMPLATE_CACHE
    if _TEMPLATE_CACHE is not None:
        return _TEMPLATE_CACHE

    path = _templates_path()
    if not path.exists():
        logger.warning(
            "[procgen] Templates missing (operation=load_templates, path=%s)", path
        )
        _TEMPLATE_CACHE = {}
        return _TEMPLATE_CACHE

    with path.open(encoding="utf-8") as fh:
        _TEMPLATE_CACHE = yaml.safe_load(fh) or {}
    return _TEMPLATE_CACHE


def _pick_unique(rng: random.Random, pool: list[Any], count: int) -> list[Any]:
    """Sample up to count unique items from pool."""
    if count <= 0 or not pool:
        return []
    count = min(count, len(pool))
    return rng.sample(pool, count)


def _build_procedural_npcs(
    rng: random.Random,
    templates: dict[str, Any],
    count: int,
) -> list[dict[str, Any]]:
    """Generate procedural villagers with deterministic ids."""
    given = templates.get("name_given", [])
    family = templates.get("name_family", [])
    roles = templates.get("villager_roles", ["villager"])
    traits = templates.get("trait_pool", [])

    npcs: list[dict[str, Any]] = []
    used_names: set[str] = set()
    for idx in range(count):
        for _ in range(20):
            name = f"{rng.choice(given)} {rng.choice(family)}"
            if name not in used_names:
                used_names.add(name)
                break
        role = rng.choice(roles)
        npc_traits = _pick_unique(rng, traits, 2)
        npcs.append(
            {
                "id": f"npc_villager_{idx + 1}",
                "name": name,
                "role": role,
                "location_id": "edgewood_square",
                "traits": npc_traits,
                "canon": False,
            }
        )
    return npcs


def _build_procedural_buildings(
    rng: random.Random,
    templates: dict[str, Any],
    count: int,
) -> list[dict[str, Any]]:
    """Generate procedural village buildings."""
    types = templates.get("building_types", [])
    picked = _pick_unique(rng, types, count)
    buildings: list[dict[str, Any]] = []
    for idx, entry in enumerate(picked):
        prefix = str(entry.get("prefix", "")).strip()
        suffix = str(entry.get("suffix", "Building"))
        name = f"{prefix} {suffix}".strip() if prefix else suffix
        btype = str(entry.get("type", "civic"))
        buildings.append(
            {
                "id": f"building_proc_{idx + 1}",
                "name": name,
                "type": btype,
                "location_id": "edgewood_square",
                "canon": False,
            }
        )
    return buildings


def _build_forest(rng: random.Random, templates: dict[str, Any]) -> dict[str, Any]:
    """Generate forest margin features."""
    counts = templates.get("counts", {})
    resources = templates.get("forage_resources", ["mushroom"])
    barrow_names = templates.get("barrow_names", ["Hollow Hill"])

    forage_nodes = []
    for idx in range(int(counts.get("forage_nodes", 6))):
        forage_nodes.append(
            {
                "id": f"forage_{idx + 1}",
                "resource": rng.choice(resources),
                "dc": rng.randint(6, 14),
                "location_id": "forest_clearing",
            }
        )

    hidden_paths = []
    for idx in range(int(counts.get("hidden_paths", 2))):
        hidden_paths.append(
            {
                "id": f"hidden_path_{idx + 1}",
                "label": rng.choice(
                    ["deer track", "mossy shortcut", "root-choked gap", "dry creek bed"]
                ),
                "leads_to": rng.choice(["deeper_forest", "old_barrows", "herb_glen"]),
                "dc": rng.randint(10, 16),
            }
        )

    barrow = {
        "id": "barrow_dungeon",
        "name": rng.choice(barrow_names),
        "optional": True,
        "dc": rng.randint(12, 16),
        "location_id": "forest_clearing",
    }

    return {
        "forage_nodes": forage_nodes,
        "hidden_paths": hidden_paths,
        "barrow_dungeon": barrow,
    }


def _build_festival(rng: random.Random, templates: dict[str, Any]) -> dict[str, Any]:
    """Pick one seasonal festival."""
    names = templates.get("festival_names", ["Harvest Lantern"])
    seasons = templates.get("festival_seasons", ["autumn"])
    return {
        "name": rng.choice(names),
        "season": rng.choice(seasons),
        "day_offset": rng.randint(14, 56),
    }


def generate_world(seed: int) -> ProcgenResult:
    """
    Generate a full procgen snapshot for the given seed.

    Args:
        seed: Deterministic RNG seed.

    Returns:
        ProcgenResult with NPCs, buildings, forest, and festival data.
    """
    templates = load_templates()
    rng = random.Random(seed)
    counts = templates.get("counts", {})

    canon_npcs = [
        {**npc, "canon": True}
        for npc in templates.get("canon_npcs", [])
    ]
    proc_npc_count = int(counts.get("procedural_npcs", 3))
    procedural_npcs = _build_procedural_npcs(rng, templates, proc_npc_count)
    npcs = canon_npcs + procedural_npcs

    canon_buildings = [
        {**b, "canon": True}
        for b in templates.get("canon_buildings", [])
    ]
    target_buildings = int(counts.get("buildings", 12))
    proc_building_count = max(0, target_buildings - len(canon_buildings))
    procedural_buildings = _build_procedural_buildings(
        rng,
        templates,
        proc_building_count,
    )
    buildings = canon_buildings + procedural_buildings

    murals = templates.get("mural_fragments", [])
    shrine_mural = rng.choice(murals) if murals else ""
    bakery_job_day = int(templates.get("bakery_job_day", 3))

    result = ProcgenResult(
        seed=seed,
        npcs=npcs,
        buildings=buildings,
        forest=_build_forest(rng, templates),
        festival=_build_festival(rng, templates),
        shrine_mural=shrine_mural,
        bakery_job_day=bakery_job_day,
    )

    logger.info(
        "[procgen] World generated (operation=generate_world, seed=%s, npcs=%s, buildings=%s)",
        seed,
        len(npcs),
        len(buildings),
    )
    return result


def npcs_at_location(procgen: ProcgenResult, location_id: str) -> list[dict[str, Any]]:
    """Return NPCs assigned to a location."""
    return [n for n in procgen.npcs if n.get("location_id") == location_id]


def npc_by_id(procgen: ProcgenResult, npc_id: str) -> Optional[dict[str, Any]]:
    """Lookup NPC by canonical id."""
    for npc in procgen.npcs:
        if npc.get("id") == npc_id:
            return npc
    return None


def populate_state(state: GameState, seed: Optional[int] = None) -> ProcgenResult:
    """
    Attach procgen data to an existing GameState.

    Args:
        state: Mutable game state.
        seed: Optional seed; random if omitted.

    Returns:
        Generated ProcgenResult attached to state.
    """
    effective_seed = seed if seed is not None else secrets.randbelow(2**31 - 1)
    procgen = generate_world(effective_seed)
    state.procgen = procgen
    return procgen


def new_game_state(
    *,
    player_name: str = "Traveler",
    archetype: str = "wayfarer",
    seed: Optional[int] = None,
    location_id: str = "forest_clearing",
) -> GameState:
    """
    Create a new session with procgen-populated world.

    Args:
        player_name: Player display name.
        archetype: Starting archetype id.
        seed: Optional deterministic seed.
        location_id: Starting location (default forest edge).

    Returns:
        Fresh GameState ready for play.
    """
    state = GameState(
        player_name=player_name,
        archetype=archetype,
        location_id=location_id,
    )
    populate_state(state, seed=seed)
    return state