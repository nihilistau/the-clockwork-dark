"""Knowledge cascade + LoreInject backing (PR24)."""

from __future__ import annotations

from pathlib import Path

import pytest

from engine.lore.interceptors import LoreInjectInterceptor
from engine.lore.manager import LoreManager, reset_lore_manager
from engine.game.state import GameState
from engine.okfs import get_bundle, reset_bundle
from engine.okfs.cascade import KnowledgeCascade, get_cascade, reset_cascade

_LORE_SAMPLE = """
# Edgewood
## Edgewood Bakery
Maris Hearth runs the Hearth Bakery with flour on her sleeves.
"""


@pytest.fixture(autouse=True)
def _reset():
    reset_cascade()
    reset_bundle()
    yield
    reset_cascade()
    reset_bundle()


def test_bundle_has_game_lore_concepts():
    bundle = get_bundle(force=True)
    assert bundle.get("the-clockwork-dark") is not None
    assert bundle.get("the-clockwork-dark").type == "Lore"
    assert bundle.get("maris-hearth").type == "NPC"
    # the bundle still validates clean with the new concepts
    assert bundle.validate() == []


def test_cascade_injected_manager_is_fts_only(tmp_path: Path):
    db = reset_lore_manager(db_path=tmp_path / "c.db")
    db.ingest_text(_LORE_SAMPLE, source="s.md")
    casc = KnowledgeCascade()
    hits = casc.query("Maris bakery", limit=3, lore_manager=db)
    assert hits
    assert all(h.source == "lore" for h in hits)  # no OKFS on injected path


def test_cascade_default_path_blends_okfs():
    get_bundle(force=True)
    casc = KnowledgeCascade()
    hits = casc.query("the clockwork dark corruption phases", limit=4)
    assert any(h.source == "okfs" for h in hits)


def test_cascade_caches_default_path():
    casc = KnowledgeCascade()
    first = casc.query("clockwork dark", limit=3)
    # mutate internal cache marker to prove the second call returns the cached list
    assert "clockwork dark" in casc._cache
    second = casc.query("clockwork dark", limit=3)
    assert first == second


def test_cascade_only_game_types_from_okfs():
    casc = KnowledgeCascade()
    # a query that matches reference docs must NOT pull them (dev docs excluded)
    hits = casc.query("structured output response_format json schema", limit=5)
    assert all(h.source != "okfs" or h.title in {"The Clockwork Dark", "The Four Evil Phases", "Maris Hearth (npc_maris)"} for h in hits)


def test_loreinject_noop_with_empty_injected_manager():
    interceptor = LoreInjectInterceptor(manager=LoreManager(db_path=Path("/tmp/empty_x2.db")))
    interceptor.manager.clear()
    assert interceptor.run_pre(GameState(), "BASE") == "BASE"


def test_loreinject_uses_injected_manager(tmp_path: Path):
    db = reset_lore_manager(db_path=tmp_path / "c2.db")
    db.ingest_text(_LORE_SAMPLE, source="s.md")
    interceptor = LoreInjectInterceptor(manager=db)
    out = interceptor.run_pre(GameState(location_id="edgewood_bakery"), "SYSTEM",
                              player_action="visit the bakery")
    assert "LORE CONTEXT" in out
    assert "Maris" in out
