"""
OKFS Bundle (PR22)
==================

Loads a directory tree of :class:`Concept` files into an in-memory, queryable
knowledge graph: lookup by slug, filter by type/tag, follow ``[[links]]`` for
progressive disclosure, and validate (required frontmatter + no broken links).

A bundle is the substrate the agents read from (Phase 3 query cascade) and the
home for lore, NPCs, items, runbooks, metrics, API docs, datasets and tables.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

from engine.config import get_config
from engine.okfs.concept import Concept

logger = logging.getLogger(__name__)

_ROOT = Path(__file__).resolve().parents[2]
_bundle_cache: Optional["OKFSBundle"] = None


class OKFSBundle:
    """An in-memory index of OKFS concepts under a root directory."""

    def __init__(self, root: Path | str) -> None:
        self.root = Path(root)
        self.concepts: dict[str, Concept] = {}
        self._load()

    def _load(self) -> None:
        if not self.root.is_dir():
            logger.warning("[okfs] Bundle root missing (operation=load, path=%s)", self.root)
            return
        for path in sorted(self.root.rglob("*.md")):
            concept = Concept.from_file(path)
            if concept.slug in self.concepts:
                logger.warning("[okfs] Duplicate slug '%s' (%s)", concept.slug, path)
            self.concepts[concept.slug] = concept

    # --- access ----------------------------------------------------------
    def __len__(self) -> int:
        return len(self.concepts)

    def get(self, slug: str) -> Optional[Concept]:
        return self.concepts.get(slug)

    def by_type(self, type_name: str) -> list[Concept]:
        return [c for c in self.concepts.values() if c.type == type_name]

    def by_tag(self, tag: str) -> list[Concept]:
        return [c for c in self.concepts.values() if tag in c.tags]

    def neighbors(self, slug: str) -> list[Concept]:
        """Concepts directly linked from ``slug`` (progressive disclosure)."""
        concept = self.get(slug)
        if not concept:
            return []
        return [self.concepts[s] for s in concept.links if s in self.concepts]

    def search(self, query: str, *, limit: int = 5) -> list[Concept]:
        """Lightweight term-overlap search over title/description/tags/body."""
        terms = [t for t in _normalize(query).split() if len(t) > 2]
        if not terms:
            return []
        scored: list[tuple[float, Concept]] = []
        for c in self.concepts.values():
            hay_title = _normalize(f"{c.title} {c.description} {' '.join(c.tags)} {c.slug}")
            hay_body = _normalize(c.body)
            score = 0.0
            for t in terms:
                if t in hay_title:
                    score += 2.0
                elif t in hay_body:
                    score += 1.0
            if score > 0:
                scored.append((score, c))
        scored.sort(key=lambda s: s[0], reverse=True)
        return [c for _s, c in scored[:limit]]

    # --- index / hashing -------------------------------------------------
    def manifest(self) -> dict[str, Any]:
        """A deterministic, content-hashed index of the bundle (the OKFS lockfile).

        Used by `scripts/build_okfs_index.py` to write `knowledge/_index.json` and
        by tests to detect drift.
        """
        import hashlib

        concepts = []
        for slug in sorted(self.concepts):
            c = self.concepts[slug]
            concepts.append(
                {
                    "slug": c.slug,
                    "type": c.type,
                    "title": c.title,
                    "tags": list(c.tags),
                    "links": list(c.links),
                    "hash": c.content_hash(),
                }
            )
        digest = hashlib.sha256(
            "\n".join(f"{c['slug']}:{c['hash']}" for c in concepts).encode("utf-8")
        ).hexdigest()[:16]
        return {"count": len(concepts), "bundle_hash": digest, "concepts": concepts}

    # --- validation ------------------------------------------------------
    def validate(self) -> list[tuple[str, str]]:
        """Return (slug, problem) for missing required fields + broken links."""
        problems: list[tuple[str, str]] = []
        for slug, c in self.concepts.items():
            for missing in c.missing_fields():
                problems.append((slug, f"missing frontmatter field: {missing}"))
            for link in c.links:
                if link not in self.concepts:
                    problems.append((slug, f"broken link: [[{link}]]"))
        return problems


def _normalize(text: str) -> str:
    return "".join(ch.lower() if ch.isalnum() else " " for ch in (text or ""))


def get_bundle(*, force: bool = False) -> OKFSBundle:
    """Process-wide knowledge bundle, rooted at ``paths.knowledge``."""
    global _bundle_cache
    if _bundle_cache is None or force:
        rel = get_config().get("paths.knowledge", "knowledge")
        _bundle_cache = OKFSBundle(_ROOT / rel)
    return _bundle_cache


def reset_bundle() -> None:
    """Clear the cached bundle (tests)."""
    global _bundle_cache
    _bundle_cache = None
