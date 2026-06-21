#!/usr/bin/env python3
"""
Sync world content from Design_files/ui_kits/clockwork-world/data.js
into data/world/content.yaml.

Usage:
    python scripts/sync_world_content.py
    python scripts/sync_world_content.py --dry-run
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml

_ROOT = Path(__file__).resolve().parents[1]
_DEFAULT_DATA_JS = Path(r"C:\Projects\clockwork-dark\Design_files\ui_kits\clockwork-world\data.js")
_OUTPUT = _ROOT / "data" / "world" / "content.yaml"


def _design_data_js() -> Path:
    env = __import__("os").environ.get("CLOCKWORK_DESIGN_FILES", "")
    if env:
        candidate = Path(env) / "ui_kits" / "clockwork-world" / "data.js"
        if candidate.exists():
            return candidate
    for candidate in (
        _DEFAULT_DATA_JS,
        _ROOT.parent / "Design_files" / "ui_kits" / "clockwork-world" / "data.js",
        _ROOT / "Design_files" / "ui_kits" / "clockwork-world" / "data.js",
    ):
        if candidate.exists():
            return candidate
    return _DEFAULT_DATA_JS


def _parse_via_node(source: Path) -> dict[str, Any] | None:
    """Parse data.js with Node when available."""
    script = """
const fs = require('fs');
const vm = require('vm');
const src = fs.readFileSync(process.argv[1], 'utf8');
const sandbox = { window: {} };
vm.runInNewContext(src, sandbox);
process.stdout.write(JSON.stringify(sandbox.window.CW_DATA || {}));
"""
    try:
        proc = subprocess.run(
            ["node", "-e", script, str(source)],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None
    if proc.returncode != 0 or not proc.stdout.strip():
        return None
    return json.loads(proc.stdout)


def _strip_js_string(value: str) -> str:
    return value.replace("\\u2014", "—").replace("\\u00b7", "·")


def _parse_array_block(text: str, key: str) -> list[dict[str, Any]]:
    """Best-effort regex parser for `key: [ { ... }, ... ]` blocks."""
    pattern = rf"{key}\s*:\s*\[(.*?)\n\s*\],"
    match = re.search(pattern, text, re.DOTALL)
    if not match:
        return []
    block = match.group(1)
    entries: list[dict[str, Any]] = []
    for obj_match in re.finditer(r"\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}", block):
        raw = obj_match.group(1)
        entry: dict[str, Any] = {}
        for field_match in re.finditer(
            r'(\w+)\s*:\s*(?:"([^"]*)"|\'([^\']*)\'|([^,\n]+))',
            raw,
        ):
            key_name = field_match.group(1)
            value = (
                field_match.group(2)
                or field_match.group(3)
                or (field_match.group(4) or "").strip()
            )
            value = _strip_js_string(value.strip().strip(","))
            if value in ("true", "false"):
                entry[key_name] = value == "true"
            elif value.isdigit():
                entry[key_name] = int(value)
            else:
                entry[key_name] = value
        if entry:
            entries.append(entry)
    return entries


def _parse_via_regex(source: Path) -> dict[str, Any]:
    text = source.read_text(encoding="utf-8")
    return {
        "places": _parse_array_block(text, "places"),
        "npcs": _parse_array_block(text, "npcs"),
        "archetypes": _parse_array_block(text, "archetypes"),
        "bestiary": _parse_array_block(text, "bestiary"),
        "assistantForms": _parse_array_block(text, "assistantForms"),
        "robes": _parse_array_block(text, "robes"),
        "items": _parse_array_block(text, "items"),
        "rumors": _parse_array_block(text, "rumors"),
        "mural": _parse_array_block(text, "mural"),
        "weather": _parse_array_block(text, "weather"),
        "phases": _parse_array_block(text, "phases"),
    }


def _normalize_img(path: str | None) -> str:
    if not path:
        return ""
    clean = path.replace("\\", "/")
    clean = clean.replace("../../assets/", "assets/")
    return clean.lstrip("/")


def _normalize_place(entry: dict[str, Any]) -> dict[str, Any]:
    out = {
        "id": entry.get("id", ""),
        "name": entry.get("name", ""),
        "kind": entry.get("kind", ""),
        "caption": entry.get("caption", ""),
        "blurb": entry.get("blurb", ""),
        "corrupted": bool(entry.get("corrupted", False)),
        "image": _normalize_img(str(entry.get("img", ""))),
        "min_phase": _phase_gate(entry),
        "requires_discovery": entry.get("id") in {"hollow_hill"},
    }
    if entry.get("note"):
        out["note"] = entry["note"]
    return out


def _phase_gate(entry: dict[str, Any]) -> str:
    caption = str(entry.get("caption", "")).upper()
    times = str(entry.get("times", "")).upper()
    if "CONSUMING" in caption or "CONSUMING" in times:
        return "consuming"
    if "SPREADING" in caption or "SPREADING" in times:
        return "spreading"
    return "dormant"


def _normalize_npc(entry: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": entry.get("id", ""),
        "name": entry.get("name", ""),
        "role": entry.get("role", ""),
        "mood": entry.get("mood", ""),
        "blurb": entry.get("blurb", ""),
        "voice": entry.get("voice", ""),
        "image": _normalize_img(str(entry.get("img", ""))),
        "ambiguous": bool(entry.get("ambiguous", False)),
    }


def _normalize_item(entry: dict[str, Any]) -> dict[str, Any]:
    return {
        "name": entry.get("name", ""),
        "tag": entry.get("tag", ""),
        "price": entry.get("price", ""),
        "from": entry.get("from", ""),
        "image": _normalize_img(str(entry.get("img", ""))),
        "brass": bool(entry.get("brass", False)),
        "corrupted": bool(entry.get("corrupted", False)),
    }


def _build_cutscene_map() -> dict[str, str]:
    return {
        "forest_clearing": "cutscene_stirring_phase",
        "edgewood_bakery": "cutscene_bakery",
        "tinker_caravan": "cutscene_tinker_map",
        "millhaven_gate": "cutscene_closing_gates",
        "corruption_border": "cutscene_consuming_horizon",
        "edgewood_shrine": "cutscene_notice_board",
        "hollow_hill": "cutscene_hidden_tunnel",
        "marches_road": "cutscene_spider_wheat",
        "ruins_temple": "cutscene_ruins",
        "clockwork_tower": "cutscene_tower",
        "forest_vines": "cutscene_clockwork_vines",
        "forest_poison": "cutscene_poison_fog",
        "notice_board": "cutscene_notice_board",
        "wheatfield_warning": "cutscene_blueprint",
    }


def _build_overlay_map() -> dict[str, str]:
    return {
        "edgewood_bakery": "bakery",
        "tinker_caravan": "trade",
        "tinker_camp": "trade",
        "edgewood_square": "notice",
        "notice_board": "notice",
        "edgewood_shrine": "shrine",
        "millhaven_gate": "militia",
    }


def _build_scene_graph() -> dict[str, list[dict[str, Any]]]:
    """Travel edges aligned with DESIGN.md location graph."""
    edges: dict[str, list[dict[str, Any]]] = {
        "forest_clearing": [
            {"to": "edgewood_square", "hours": 1, "danger_dc": 8, "awareness_delta": 0},
            {"to": "forest_forage", "hours": 1, "danger_dc": 10, "awareness_delta": 0},
            {"to": "resting_camp", "hours": 2, "danger_dc": 10, "awareness_delta": 1},
            {"to": "hollow_hill", "hours": 2, "danger_dc": 14, "awareness_delta": 2, "requires_discovery": "hidden_path"},
        ],
        "edgewood_square": [
            {"to": "forest_clearing", "hours": 1, "danger_dc": 8, "awareness_delta": 0},
            {"to": "edgewood_bakery", "hours": 0, "danger_dc": 0, "awareness_delta": 0},
            {"to": "tinker_caravan", "hours": 0, "danger_dc": 0, "awareness_delta": 1},
            {"to": "edgewood_shrine", "hours": 0, "danger_dc": 0, "awareness_delta": 0},
            {"to": "notice_board", "hours": 0, "danger_dc": 0, "awareness_delta": 0},
            {"to": "marches_road", "hours": 2, "danger_dc": 12, "awareness_delta": 2},
        ],
        "edgewood_bakery": [
            {"to": "edgewood_square", "hours": 0, "danger_dc": 0, "awareness_delta": 0},
        ],
        "tinker_caravan": [
            {"to": "edgewood_square", "hours": 0, "danger_dc": 0, "awareness_delta": 0},
            {"to": "tinker_camp", "hours": 1, "danger_dc": 8, "awareness_delta": 0},
        ],
        "tinker_camp": [
            {"to": "tinker_caravan", "hours": 1, "danger_dc": 8, "awareness_delta": 0},
        ],
        "notice_board": [
            {"to": "edgewood_square", "hours": 0, "danger_dc": 0, "awareness_delta": 0},
        ],
        "edgewood_shrine": [
            {"to": "edgewood_square", "hours": 0, "danger_dc": 0, "awareness_delta": 0},
        ],
        "forest_forage": [
            {"to": "forest_clearing", "hours": 1, "danger_dc": 10, "awareness_delta": 0},
            {"to": "forest_vines", "hours": 1, "danger_dc": 12, "awareness_delta": 2, "min_phase": "stirring"},
            {"to": "forest_poison", "hours": 1, "danger_dc": 14, "awareness_delta": 3, "min_phase": "stirring"},
        ],
        "forest_vines": [
            {"to": "forest_forage", "hours": 1, "danger_dc": 12, "awareness_delta": 1},
        ],
        "forest_poison": [
            {"to": "forest_forage", "hours": 1, "danger_dc": 14, "awareness_delta": 1},
        ],
        "resting_camp": [
            {"to": "forest_clearing", "hours": 2, "danger_dc": 10, "awareness_delta": 0},
            {"to": "marches_road", "hours": 2, "danger_dc": 12, "awareness_delta": 2},
        ],
        "marches_road": [
            {"to": "edgewood_square", "hours": 2, "danger_dc": 12, "awareness_delta": 2},
            {"to": "resting_camp", "hours": 2, "danger_dc": 12, "awareness_delta": 1},
            {"to": "millhaven_gate", "hours": 2, "danger_dc": 14, "awareness_delta": 3},
            {"to": "corruption_border", "hours": 3, "danger_dc": 16, "awareness_delta": 4, "min_phase": "spreading"},
            {"to": "wheatfield_warning", "hours": 1, "danger_dc": 12, "awareness_delta": 2, "min_phase": "stirring"},
            {"to": "scarecrow_field", "hours": 1, "danger_dc": 14, "awareness_delta": 3, "min_phase": "stirring"},
        ],
        "wheatfield_warning": [
            {"to": "marches_road", "hours": 1, "danger_dc": 12, "awareness_delta": 1},
        ],
        "scarecrow_field": [
            {"to": "marches_road", "hours": 1, "danger_dc": 14, "awareness_delta": 1},
        ],
        "millhaven_gate": [
            {"to": "marches_road", "hours": 2, "danger_dc": 14, "awareness_delta": 3},
        ],
        "corruption_border": [
            {"to": "marches_road", "hours": 3, "danger_dc": 16, "awareness_delta": 4},
            {"to": "clockwork_tower", "hours": 4, "danger_dc": 18, "awareness_delta": 6, "min_phase": "consuming"},
        ],
        "hollow_hill": [
            {"to": "forest_clearing", "hours": 2, "danger_dc": 14, "awareness_delta": 2},
            {"to": "ruins_temple", "hours": 3, "danger_dc": 16, "awareness_delta": 4},
        ],
        "ruins_temple": [
            {"to": "hollow_hill", "hours": 3, "danger_dc": 16, "awareness_delta": 4},
        ],
        "clockwork_tower": [
            {"to": "corruption_border", "hours": 4, "danger_dc": 18, "awareness_delta": 6},
        ],
        "hurt_rest": [
            {"to": "resting_camp", "hours": 0, "danger_dc": 0, "awareness_delta": 0},
        ],
    }
    return edges


def build_content(source: Path) -> dict[str, Any]:
    raw = _parse_via_node(source) or _parse_via_regex(source)
    places = [_normalize_place(p) for p in raw.get("places", []) if p.get("id")]
    npcs = [_normalize_npc(n) for n in raw.get("npcs", []) if n.get("id")]
    items = [_normalize_item(i) for i in raw.get("items", []) if i.get("name")]
    return {
        "version": 1,
        "source": str(source),
        "places": places,
        "npcs": npcs,
        "archetypes": raw.get("archetypes", []),
        "bestiary": raw.get("bestiary", []),
        "assistant_forms": raw.get("assistantForms", []),
        "robes": raw.get("robes", []),
        "items": items,
        "rumors": raw.get("rumors", []),
        "mural": raw.get("mural", []),
        "weather": raw.get("weather", []),
        "phases": raw.get("phases", []),
        "cutscene_map": _build_cutscene_map(),
        "overlay_map": _build_overlay_map(),
        "scene_graph": _build_scene_graph(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync world content from data.js")
    parser.add_argument("--dry-run", action="store_true", help="Print summary only")
    parser.add_argument("--output", type=Path, default=_OUTPUT)
    args = parser.parse_args()

    source = _design_data_js()
    if not source.exists():
        print(f"[sync_world_content] data.js not found: {source}", file=sys.stderr)
        return 1

    content = build_content(source)
    summary = (
        f"places={len(content['places'])} npcs={len(content['npcs'])} "
        f"items={len(content['items'])} edges="
        f"{sum(len(v) for v in content['scene_graph'].values())}"
    )
    print(f"[sync_world_content] Parsed {summary} from {source.name}")

    if args.dry_run:
        return 0

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as fh:
        yaml.safe_dump(content, fh, sort_keys=False, allow_unicode=True)
    print(f"[sync_world_content] Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())