"""
Knowledge Cascade (PR24)
========================

A small confidence cascade unifying retrieval for the agents (CosySim
NexusQueryRouter, slimmed): an in-memory cache → the game-lore FTS store
(`LoreManager`) → the OKFS bundle (game-relevant concept types). Results are
deduped by title and cached.

Backing for `LoreInjectInterceptor`. When a *specific* lore manager is injected
(tests / explicit wiring) the cascade stays FTS-only on that manager — the OKFS
blend and cache apply only on the default gameplay path.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

# OKFS concept types that may enrich an in-character prompt (dev/reference docs
# are deliberately excluded so they never leak into the GM context).
_GAME_TYPES = {"Lore", "NPC", "Item", "Location", "Bestiary", "Phase", "Faction"}


@dataclass
class KnowledgeHit:
    title: str
    text: str
    source: str  # "lore" | "okfs"
    score: float = 0.0


class KnowledgeCascade:
    """Cache → lore FTS → OKFS game concepts."""

    def __init__(self, *, cache_size: int = 128) -> None:
        self._cache: dict[str, list[KnowledgeHit]] = {}
        self._order: list[str] = []
        self._cache_size = cache_size

    def query(
        self,
        text: str,
        *,
        limit: int = 3,
        lore_manager: Optional[Any] = None,
    ) -> list[KnowledgeHit]:
        # Injected manager → legacy FTS-only (no OKFS, no cache).
        if lore_manager is not None:
            return self._fts(text, lore_manager, limit)

        key = text.strip().lower()
        cached = self._cache.get(key)
        if cached is not None:
            return cached[:limit]

        from engine.lore.manager import get_lore_manager

        hits = self._fts(text, get_lore_manager(), limit) + self._okfs(text, limit)
        seen: set[str] = set()
        out: list[KnowledgeHit] = []
        for h in hits:
            k = h.title.lower()
            if k not in seen:
                seen.add(k)
                out.append(h)
        self._store(key, out)
        return out[:limit]

    @staticmethod
    def _fts(text: str, manager: Any, limit: int) -> list[KnowledgeHit]:
        out: list[KnowledgeHit] = []
        try:
            if manager.count() == 0:
                return out
            for c in manager.search(text, limit=limit):
                out.append(KnowledgeHit(c.title, c.text, "lore", 2.0))
        except Exception:
            pass
        return out

    @staticmethod
    def _okfs(text: str, limit: int) -> list[KnowledgeHit]:
        out: list[KnowledgeHit] = []
        try:
            from engine.okfs import get_bundle

            for c in get_bundle().search(text, limit=limit):
                if c.type in _GAME_TYPES:
                    out.append(
                        KnowledgeHit(c.title, c.description or c.body[:240], "okfs", 1.5)
                    )
        except Exception:
            pass
        return out

    def _store(self, key: str, val: list[KnowledgeHit]) -> None:
        self._cache[key] = val
        self._order.append(key)
        if len(self._order) > self._cache_size:
            self._cache.pop(self._order.pop(0), None)


_cascade: Optional[KnowledgeCascade] = None


def get_cascade() -> KnowledgeCascade:
    global _cascade
    if _cascade is None:
        _cascade = KnowledgeCascade()
    return _cascade


def reset_cascade() -> None:
    global _cascade
    _cascade = None
