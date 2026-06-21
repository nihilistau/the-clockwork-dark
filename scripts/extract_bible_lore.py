"""
Extract Lore from Design Bible
==============================

Reads ui_kits/clockwork-world/data.js from Design_files and writes
data/lore/*.md chunks for RAG seeding. Uses a lightweight line scanner
(no heavy regex) to avoid hangs on large bundled files.

Usage:
    python scripts/extract_bible_lore.py
    python scripts/extract_bible_lore.py --design-root C:\\Projects\\clockwork-dark\\Design_files
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from engine.design.assets import get_design_root

_FIELD_RE = re.compile(r'^\s*(id|name|role|kind|blurb|text|frag|phase|form|note|reads):\s*"(.*)",?\s*$')


def _read_data_js(design_root: Path) -> list[str]:
    path = design_root / "ui_kits" / "clockwork-world" / "data.js"
    if not path.exists():
        raise FileNotFoundError(f"data.js not found at {path}")
    return path.read_text(encoding="utf-8").splitlines()


def _scan_array(lines: list[str], start_key: str) -> list[dict[str, str]]:
    """Scan objects inside `key: [` until matching `],`."""
    entries: list[dict[str, str]] = []
    in_array = False
    depth = 0
    current: dict[str, str] = {}

    for line in lines:
        if not in_array:
            if line.strip().startswith(f"{start_key}:") and "[" in line:
                in_array = True
                depth = line.count("[") - line.count("]")
            continue

        depth += line.count("[") - line.count("]")
        if depth <= 0 and line.strip().endswith("],"):
            if current:
                entries.append(current)
            break

        if "{" in line:
            if current:
                entries.append(current)
            current = {}
            continue
        if "}" in line:
            if current:
                entries.append(current)
            current = {}
            continue

        m = _FIELD_RE.match(line)
        if m and current is not None:
            current[m.group(1)] = m.group(2)

    return entries


def _write_md(
    path: Path,
    title: str,
    sections: list[tuple[str, str, str]],
    *,
    min_sections: int = 1,
) -> int:
    """Write markdown only when enough sections were parsed (avoid clobbering curated lore)."""
    valid = [s for s in sections if s[0].strip()]
    if len(valid) < min_sections:
        print(f"[extract_bible_lore] Skipped {path.name} ({len(valid)} sections parsed)")
        return 0
    lines = [f"# {title}\n"]
    for heading, sub, body in valid:
        lines.append(f"## {heading}\n")
        if sub:
            lines.append(f"*{sub}*\n")
        if body:
            lines.append(f"{body}\n")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")
    return len(valid)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Extract lore markdown from Design_files data.js")
    parser.add_argument("--design-root", type=str, default=None)
    parser.add_argument("--out", type=str, default="data/lore")
    args = parser.parse_args(argv)

    design_root = Path(args.design_root) if args.design_root else get_design_root()
    if design_root is None or not design_root.is_dir():
        print("[extract_bible_lore] Design_files not found.", file=sys.stderr)
        return 1

    lines = _read_data_js(design_root)
    out_dir = _ROOT / args.out
    out_dir.mkdir(parents=True, exist_ok=True)

    places = _scan_array(lines, "places")
    npcs = _scan_array(lines, "npcs")
    bestiary = _scan_array(lines, "bestiary")
    rumors = _scan_array(lines, "rumors")
    mural = _scan_array(lines, "mural")
    phases = _scan_array(lines, "phases")
    forms = _scan_array(lines, "assistantForms")
    robes = _scan_array(lines, "robes")

    counts = {
        "places": _write_md(
            out_dir / "places.md",
            "Places of the Margin",
            [(p.get("name", p.get("id", "")), p.get("kind", ""), p.get("blurb", "")) for p in places],
        ),
        "npcs": _write_md(
            out_dir / "npcs.md",
            "Souls of Edgewood",
            [(n.get("name", ""), n.get("role", ""), n.get("blurb", "")) for n in npcs],
        ),
        "bestiary": _write_md(
            out_dir / "bestiary.md",
            "Bestiary",
            [(b.get("name", ""), "", b.get("blurb", "")) for b in bestiary],
        ),
        "assistant": _write_md(
            out_dir / "assistant.md",
            "The Assistant",
            [(f.get("form", "").title(), f.get("when", ""), f.get("note", "")) for f in forms]
            + [(r.get("name", ""), r.get("reads", ""), r.get("blurb", "")) for r in robes],
        ),
    }

    rumor_count = len(rumors) + len(mural) + len(phases)
    if rumor_count >= 3:
        rumor_lines = ["# Rumors, Mural, and Phases\n", "## Village Rumors\n"]
        for r in rumors:
            rumor_lines.append(f"- ({r.get('phase', '')}) {r.get('text', '')}")
        rumor_lines.append("\n## Shrine Mural Fragments\n")
        for m in mural:
            rumor_lines.append(f"- **{m.get('phase', '')}**: {m.get('frag', '')}")
        rumor_lines.append("\n## Evil Phases\n")
        for p in phases:
            rumor_lines.append(f"## {p.get('label', p.get('key', ''))}\n")
            rumor_lines.append(f"{p.get('mood', '')}\n")
            rumor_lines.append(f"{p.get('ui', '')}\n\n")
        (out_dir / "rumors_and_phases.md").write_text("\n".join(rumor_lines), encoding="utf-8")
        counts["rumors"] = rumor_count
    else:
        print("[extract_bible_lore] Skipped rumors_and_phases.md (parser found too few entries)")
        counts["rumors"] = 0

    print(f"[extract_bible_lore] Wrote {counts} sections to {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())