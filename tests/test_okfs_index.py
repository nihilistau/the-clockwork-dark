"""OKFS hashing + index lockfile (PR32)."""

from __future__ import annotations

import json
from pathlib import Path

from engine.okfs import Concept, get_bundle, reset_bundle

_ROOT = Path(__file__).resolve().parents[1]
_INDEX = _ROOT / "knowledge" / "_index.json"


def test_content_hash_is_stable_and_content_addressed():
    a = Concept.from_text("x", "---\ntype: Lore\ntitle: T\ndescription: d\n---\nBody one.")
    b = Concept.from_text("y", "---\ntype: Lore\ntitle: T\ndescription: d\n---\nBody one.")
    c = Concept.from_text("x", "---\ntype: Lore\ntitle: T\ndescription: d\n---\nBody TWO.")
    assert a.content_hash() == b.content_hash()      # same substance -> same hash
    assert a.content_hash() != c.content_hash()      # changed body -> changed hash
    assert len(a.content_hash()) == 16


def test_manifest_shape():
    reset_bundle()
    m = get_bundle(force=True).manifest()
    assert m["count"] == len(m["concepts"])
    assert len(m["bundle_hash"]) == 16
    slugs = [c["slug"] for c in m["concepts"]]
    assert slugs == sorted(slugs)                    # deterministic order
    for c in m["concepts"]:
        assert {"slug", "type", "title", "tags", "links", "hash"} <= set(c)


def test_committed_index_is_current():
    """`knowledge/_index.json` must match the bundle. Stale? run
    `python scripts/build_okfs_index.py`."""
    assert _INDEX.exists(), "knowledge/_index.json missing — run build_okfs_index.py"
    committed = json.loads(_INDEX.read_text(encoding="utf-8"))
    reset_bundle()
    live = get_bundle(force=True).manifest()
    assert committed == live, "OKFS index is stale — run python scripts/build_okfs_index.py"


def test_changelog_present():
    bundle = get_bundle(force=True)
    cl = bundle.get("changelog")
    assert cl is not None and cl.type == "Log"
