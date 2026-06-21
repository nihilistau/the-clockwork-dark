#!/usr/bin/env python3
"""
Build or refresh data/assets/manifest.yaml from Design_files on disk.

Scans scenes, souls, enemies, things, video, dice, and HUD cutouts.
Merges with existing manifest entries (preserves captions/metadata).

Usage:
    python scripts/build_asset_manifest.py
    python scripts/build_asset_manifest.py --dry-run
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

import yaml

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from engine.design.assets import get_design_root, reset_design_cache
_MANIFEST = _ROOT / "data" / "assets" / "manifest.yaml"

_SCENE_MAP = {
    "forest-mushroom-ring": "forest_clearing",
    "town-scene": "edgewood_square",
    "bakery": "edgewood_bakery",
    "tinker-cart": "tinker_caravan",
    "tinker-camping": "tinker_camp",
    "closing-town-gates": "millhaven_gate",
    "clockwork-wheatfield": "corruption_border",
    "noticeboard": "edgewood_shrine",
    "forest-hidden-tunnel": "hollow_hill",
    "wheatfield-forest-edge": "marches_road",
    "resting-camp": "resting_camp",
    "ruins-temple-mages": "ruins_temple",
    "clockwork-tower": "clockwork_tower",
    "forest-tree-stump": "forest_forage",
    "forest-poison-gas": "forest_poison",
    "forest-clockwork-vines": "forest_vines",
    "wheatfield-drawing-warning": "wheatfield_warning",
    "wheatfields-scarecrow": "scarecrow_field",
    "player-hurt-resting": "hurt_rest",
    "noticeboard-cutscene": "notice_board",
}

_CUTSCENE_MAP = {
    "cutscene-misty-forest": "cutscene_stirring_phase",
    "forrest-mushroom-ring-cutscene": "cutscene_assistant_reveal",
    "cutscene-wheatfield": "cutscene_consuming_horizon",
    "cutscene-notice-board": "cutscene_notice_board",
    "cutscene-closing-gates": "cutscene_closing_gates",
    "cutscene-golden-ring-bread": "cutscene_golden_ring_bread",
    "cutscene-tower": "cutscene_tower",
    "city-bakery-cutscene": "cutscene_bakery",
    "tent-base-map-cutscene": "cutscene_tinker_map",
    "ruins-temple-mages-cutscene": "cutscene_ruins",
    "forrest-hidden-tunnels-cutscene": "cutscene_hidden_tunnel",
    "forrest-clockwork-vines-cutscene": "cutscene_clockwork_vines",
    "forrest-clockwork-mushroom-poison-fog": "cutscene_poison_fog",
    "wizard-vs-clockwork-enemy-cutscene": "cutscene_wizard_fight",
    "clockwork-blueprint-warning-fly-in": "cutscene_blueprint",
    "clockwork-spinerfex-wheatfield-cutscene": "cutscene_spider_wheat",
}

_ASSISTANT_MAP = {
    "cat-assistant": "cat",
    "assistant-mage": "wanderer",
    "child-assistant": "child",
    "tinker": "tinker",
    "shadow-mage-assistant": "reflection",
}

_ENEMY_MAP = {
    "wolf": "wolf",
    "scarecrow-clockwork": "scarecrow_brass",
    "scarecrow": "scarecrow",
    "clockwork-monster-vs-mage": "clockwork_beast",
    "clockwork-mage": "husk",
}


def _rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def _scan_scenes(root: Path, manifest: dict[str, Any]) -> None:
    places = manifest.setdefault("places", {})
    scenes_dir = root / "assets" / "art" / "scenes"
    if not scenes_dir.is_dir():
        return
    for img in scenes_dir.glob("*.jpg"):
        stem = img.stem
        loc_id = _SCENE_MAP.get(stem)
        if not loc_id:
            continue
        entry = places.setdefault(loc_id, {"id": loc_id})
        entry["image"] = _rel(img, root)
        if "corrupted" not in entry and "clockwork" in stem:
            entry["corrupted"] = True


def _scan_videos(root: Path, manifest: dict[str, Any]) -> None:
    cutscenes = manifest.setdefault("cutscenes", {})
    video_dir = root / "assets" / "video"
    if not video_dir.is_dir():
        return
    for vid in video_dir.rglob("*.mp4"):
        if "dice" in vid.parts:
            continue
        stem = vid.stem
        for key, cid in _CUTSCENE_MAP.items():
            if key in stem:
                entry = cutscenes.setdefault(cid, {})
                entry["video"] = _rel(vid, root)
                break


def _scan_dice(root: Path, manifest: dict[str, Any]) -> None:
    dice_dir = root / "assets" / "video" / "dice"
    if not dice_dir.is_dir():
        return
    videos = sorted(dice_dir.glob("*.mp4"))
    if not videos:
        return
    dice = manifest.setdefault("dice_videos", {})
    dice["roll"] = _rel(videos[0], root)
    for idx, vid in enumerate(videos[1:], start=2):
        dice[f"roll_{idx}"] = _rel(vid, root)
    d20_faces = sorted(dice_dir.glob("d20_*.mp4"))
    if d20_faces:
        faces: dict[str, str] = {}
        for vid in d20_faces:
            m = re.search(r"d20_(\d+)", vid.stem)
            if m:
                faces[m.group(1)] = _rel(vid, root)
        if faces:
            manifest["dice_faces"] = faces


def _scan_portraits(root: Path, manifest: dict[str, Any]) -> None:
    assistant = manifest.setdefault("assistant_forms", {})
    souls = root / "assets" / "art" / "souls"
    if souls.is_dir():
        for img in souls.glob("*.jpg"):
            form = _ASSISTANT_MAP.get(img.stem)
            if form:
                assistant.setdefault(form, {})["image"] = _rel(img, root)

    enemies = manifest.setdefault("enemies", {})
    enemies_dir = root / "assets" / "art" / "enemies"
    if enemies_dir.is_dir():
        for img in enemies_dir.glob("*.jpg"):
            eid = _ENEMY_MAP.get(img.stem, img.stem.replace("-", "_"))
            enemies.setdefault(eid, {})["image"] = _rel(img, root)

    things = root / "assets" / "art" / "things"
    if things.is_dir():
        items = manifest.setdefault("items", {})
        for img in things.glob("*.*"):
            key = img.stem.replace("-", " ").lower()
            items.setdefault(key, {})["image"] = _rel(img, root)


def _scan_hud(root: Path, manifest: dict[str, Any]) -> None:
    hud_dir = root / "assets" / "art" / "hud"
    if not hud_dir.is_dir():
        return
    hud: dict[str, str] = {}
    for img in hud_dir.glob("*.png"):
        hud[img.stem] = _rel(img, root)
    if hud:
        manifest["hud"] = hud


def build_manifest(existing: dict[str, Any], root: Path) -> dict[str, Any]:
    """Scan disk and merge into manifest."""
    manifest = dict(existing)
    _scan_scenes(root, manifest)
    _scan_videos(root, manifest)
    _scan_dice(root, manifest)
    _scan_portraits(root, manifest)
    _scan_hud(root, manifest)
    manifest["generated_by"] = "build_asset_manifest.py"
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--output", type=Path, default=_MANIFEST)
    args = parser.parse_args()

    reset_design_cache()
    root = get_design_root()
    if root is None:
        print("[build_asset_manifest] Design_files not found", file=sys.stderr)
        return 1

    existing: dict[str, Any] = {}
    if args.output.exists():
        with args.output.open(encoding="utf-8") as fh:
            existing = yaml.safe_load(fh) or {}

    manifest = build_manifest(existing, root)
    places = len(manifest.get("places", {}))
    cutscenes = len(manifest.get("cutscenes", {}))
    print(f"[build_asset_manifest] places={places} cutscenes={cutscenes} root={root}")

    if args.dry_run:
        return 0

    with args.output.open("w", encoding="utf-8") as fh:
        yaml.safe_dump(manifest, fh, sort_keys=False, allow_unicode=True)
    print(f"[build_asset_manifest] Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())