"""
Build the OKFS index/lockfile.
==============================

Writes ``knowledge/_index.json`` — a deterministic, content-hashed manifest of
every concept in the bundle. This is the OKFS "hashing system": each concept
carries a content hash, the bundle a roll-up hash, so drift is detectable and the
index is reviewable in PRs.

Run after editing concepts:  ``python scripts/build_okfs_index.py``
(``tests/test_okfs_index.py`` fails if the committed index is stale.)
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_ROOT))

from engine.okfs import get_bundle  # noqa: E402


def build() -> dict:
    bundle = get_bundle(force=True)
    manifest = bundle.manifest()
    out = _ROOT / "knowledge" / "_index.json"
    out.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest


if __name__ == "__main__":
    m = build()
    print(f"[okfs] wrote knowledge/_index.json — {m['count']} concepts, bundle_hash={m['bundle_hash']}")
