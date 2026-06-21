"""
Design Asset Resolver
=====================

Maps game ids (locations, cutscenes, assistant forms) to files under
the external Design_files tree and builds /design/... URLs for Flask.
"""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any, Optional

import yaml

from engine.config import get_config

logger = logging.getLogger(__name__)

_ROOT = Path(__file__).resolve().parents[2]
_MANIFEST_CACHE: Optional[dict[str, Any]] = None
_DESIGN_ROOT_CACHE: Optional[Optional[Path]] = None

_FALLBACK_DESIGN_ROOTS = (
    Path(r"C:\Projects\clockwork-dark\Design_files"),
    _ROOT.parent / "Design_files",
    _ROOT / "Design_files",
)


def get_design_root() -> Optional[Path]:
    """Return resolved Design_files directory, or None if unavailable."""
    global _DESIGN_ROOT_CACHE
    if _DESIGN_ROOT_CACHE is not None:
        return _DESIGN_ROOT_CACHE

    cfg_path = get_config().get("paths.design_files")
    candidates: list[Path] = []
    if cfg_path:
        raw = str(cfg_path)
        if raw.startswith("${") and raw.endswith("}"):
            env_val = os.environ.get(raw[2:-1], "")
            if env_val:
                candidates.append(Path(env_val))
        else:
            p = Path(raw)
            candidates.append(p if p.is_absolute() else _ROOT / raw)

    candidates.extend(_FALLBACK_DESIGN_ROOTS)
    for candidate in candidates:
        if candidate.is_dir():
            _DESIGN_ROOT_CACHE = candidate.resolve()
            logger.debug(
                "[design_assets] Root resolved (operation=get_design_root, path=%s)",
                _DESIGN_ROOT_CACHE,
            )
            return _DESIGN_ROOT_CACHE

    logger.warning(
        "[design_assets] Design_files not found (operation=get_design_root)"
    )
    _DESIGN_ROOT_CACHE = None
    return None


def reset_design_cache() -> None:
    """Clear caches (tests only)."""
    global _MANIFEST_CACHE, _DESIGN_ROOT_CACHE
    _MANIFEST_CACHE = None
    _DESIGN_ROOT_CACHE = None


def _manifest_path() -> Path:
    rel = get_config().get(
        "paths.asset_manifest",
        "data/assets/manifest.yaml",
    )
    return _ROOT / rel


def get_asset_manifest() -> dict[str, Any]:
    """Load and cache the asset manifest YAML."""
    global _MANIFEST_CACHE
    if _MANIFEST_CACHE is not None:
        return _MANIFEST_CACHE

    path = _manifest_path()
    if not path.exists():
        _MANIFEST_CACHE = {}
        return _MANIFEST_CACHE

    with path.open(encoding="utf-8") as fh:
        _MANIFEST_CACHE = yaml.safe_load(fh) or {}
    return _MANIFEST_CACHE


def design_url(relative_path: str) -> str:
    """
    Build a browser URL for a file under Design_files.

    Args:
        relative_path: Path relative to design root, e.g. assets/art/scenes/foo.jpg
    """
    clean = relative_path.replace("\\", "/").lstrip("/")
    return f"/design/{clean}"


def _place_entry(location_id: str) -> dict[str, Any]:
    manifest = get_asset_manifest()
    places = manifest.get("places", {})
    return dict(places.get(location_id, {}))


def resolve_location_image(location_id: str, time_of_day: str = "dawn") -> Optional[str]:
    """Return /design/ URL for a location still, if mapped."""
    place = _place_entry(location_id)
    if not place:
        return None

    times = place.get("times", {})
    if isinstance(times, dict) and time_of_day in times:
        rel = times[time_of_day]
        if rel:
            return design_url(str(rel))

    image = place.get("image")
    if image:
        return design_url(str(image))
    return None


def resolve_placeholder_image(image_tag: str) -> Optional[str]:
    """Resolve [IMAGE:tag] placeholder to a design asset URL."""
    from engine.media.queue import parse_image_tag

    location_id, time_of_day = parse_image_tag(image_tag)
    return resolve_location_image(location_id, time_of_day)


def resolve_cutscene_video(cutscene_id: str) -> Optional[str]:
    """Return /design/ URL for a cutscene video, if mapped."""
    manifest = get_asset_manifest()
    scene = manifest.get("cutscenes", {}).get(cutscene_id, {})
    video = scene.get("video")
    if video:
        return design_url(str(video))
    return None


def resolve_assistant_image(form: str) -> Optional[str]:
    """Return /design/ URL for an assistant form portrait."""
    manifest = get_asset_manifest()
    entry = manifest.get("assistant_forms", {}).get(form, {})
    image = entry.get("image")
    if image:
        return design_url(str(image))
    return None


def resolve_dice_video(outcome: str = "roll") -> Optional[str]:
    """Pick a dice animation video from the manifest."""
    manifest = get_asset_manifest()
    videos = manifest.get("dice_videos", {})
    if isinstance(videos, dict):
        rel = videos.get(outcome) or videos.get("roll")
        if rel:
            return design_url(str(rel))
    if isinstance(videos, list) and videos:
        return design_url(str(videos[0]))
    return None


def resolve_item_image(item_name: str) -> Optional[str]:
    """Return /design/ URL for an item icon by display name."""
    manifest = get_asset_manifest()
    items = manifest.get("items", {})
    entry = items.get(item_name.lower(), {})
    image = entry.get("image")
    if image:
        return design_url(str(image))
    return None


def place_metadata(location_id: str) -> dict[str, Any]:
    """Return place name, caption, and image URL for UI."""
    place = _place_entry(location_id)
    if not place:
        return {"id": location_id, "name": location_id, "caption": "", "image_url": ""}
    image_url = resolve_location_image(location_id) or ""
    return {
        "id": location_id,
        "name": place.get("name", location_id),
        "caption": place.get("caption", ""),
        "image_url": image_url,
        "kind": place.get("kind", ""),
    }


def resolve_intro_video(hd: bool = False) -> Optional[str]:
    """Return /design/ URL for the title intro video."""
    manifest = get_asset_manifest()
    intro = manifest.get("intro", {})
    key = "video_hd" if hd else "video"
    rel = intro.get(key) or intro.get("video")
    return design_url(str(rel)) if rel else None


def resolve_start_background() -> Optional[str]:
    """Return /design/ URL for the menu/title screen backdrop."""
    manifest = get_asset_manifest()
    rel = manifest.get("start_screen", {}).get("background")
    return design_url(str(rel)) if rel else None


def resolve_npc_image(npc_id: str) -> Optional[str]:
    """Return /design/ URL for an NPC portrait."""
    manifest = get_asset_manifest()
    entry = manifest.get("npcs", {}).get(npc_id, {})
    image = entry.get("image")
    if image:
        return design_url(str(image))
    return None


def resolve_hud_image(hud_id: str) -> Optional[str]:
    """Return /design/ URL for a HUD cutout asset."""
    manifest = get_asset_manifest()
    rel = manifest.get("hud", {}).get(hud_id)
    return design_url(str(rel)) if rel else None


def resolve_dice_face_video(face: int) -> Optional[str]:
    """Return /design/ URL for a specific d20 face video."""
    manifest = get_asset_manifest()
    faces = manifest.get("dice_faces", {})
    rel = faces.get(str(face)) or faces.get(f"{face:02d}")
    return design_url(str(rel)) if rel else None


def resolve_enemy_image(enemy_id: str) -> Optional[str]:
    """Return /design/ URL for a bestiary enemy still."""
    manifest = get_asset_manifest()
    entry = manifest.get("enemies", {}).get(enemy_id, {})
    image = entry.get("image")
    return design_url(str(image)) if image else None


def manifest_for_client() -> dict[str, Any]:
    """Serialize manifest with resolved URLs for the scene client."""
    manifest = get_asset_manifest()
    places: dict[str, Any] = {}
    for loc_id, place in manifest.get("places", {}).items():
        places[loc_id] = {
            **place,
            "image_url": resolve_location_image(loc_id) or "",
        }

    cutscenes: dict[str, Any] = {}
    for cid, scene in manifest.get("cutscenes", {}).items():
        cutscenes[cid] = {
            **scene,
            "video_url": resolve_cutscene_video(cid) or "",
        }

    assistant_forms: dict[str, Any] = {}
    for form, entry in manifest.get("assistant_forms", {}).items():
        assistant_forms[form] = {
            **entry,
            "image_url": resolve_assistant_image(form) or "",
        }

    dice_videos: dict[str, str] = {}
    raw_dice = manifest.get("dice_videos", {})
    if isinstance(raw_dice, dict):
        for key, rel in raw_dice.items():
            dice_videos[key] = design_url(str(rel))
    elif isinstance(raw_dice, list):
        for idx, rel in enumerate(raw_dice):
            dice_videos[f"roll_{idx}"] = design_url(str(rel))

    start = manifest.get("start_screen", {})
    intro = manifest.get("intro", {})
    archetypes: dict[str, Any] = {}
    for arch_id, arch in manifest.get("archetypes", {}).items():
        archetypes[arch_id] = dict(arch)

    enemies: dict[str, Any] = {}
    for eid, entry in manifest.get("enemies", {}).items():
        enemies[eid] = {**entry, "image_url": resolve_enemy_image(eid) or ""}

    npcs: dict[str, Any] = {}
    for nid, entry in manifest.get("npcs", {}).items():
        npcs[nid] = {**entry, "image_url": resolve_npc_image(nid) or ""}

    hud: dict[str, str] = {}
    for hid, rel in manifest.get("hud", {}).items():
        hud[hid] = design_url(str(rel))

    dice_faces: dict[str, str] = {}
    for face, rel in manifest.get("dice_faces", {}).items():
        dice_faces[face] = design_url(str(rel))

    items: dict[str, Any] = {}
    for iid, entry in manifest.get("items", {}).items():
        image = entry.get("image")
        items[iid] = {
            **entry,
            "image_url": design_url(str(image)) if image else "",
        }

    return {
        "design_available": get_design_root() is not None,
        "places": places,
        "cutscenes": cutscenes,
        "assistant_forms": assistant_forms,
        "dice_videos": dice_videos,
        "dice_faces": dice_faces,
        "enemies": enemies,
        "npcs": npcs,
        "items": items,
        "hud": hud,
        "archetypes": archetypes,
        "phases": manifest.get("phases", []),
        "intro": {
            "video_url": resolve_intro_video(hd=False) or "",
            "video_hd_url": resolve_intro_video(hd=True) or "",
        },
        "start_screen": {
            "background_url": resolve_start_background() or "",
            "wordmark_url": design_url(str(start.get("wordmark", "assets/wordmark.svg"))),
            "gear_motif_url": design_url(str(start.get("gear_motif", "assets/gear-motif.svg"))),
        },
        "brand": {
            "gear_motif": design_url("assets/gear-motif.svg"),
            "wordmark": design_url("assets/wordmark.svg"),
        },
    }