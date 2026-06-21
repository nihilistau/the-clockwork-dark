"""
OKFS Concept (PR22)
===================

One concept = one Markdown file with YAML frontmatter + a Markdown body that may
link sibling concepts with ``[[slug]]`` wiki-links. This is *our* version of the
Open Knowledge Format: git-native, agent-traversable, zero runtime lock-in.

Frontmatter (required: type, title, description):

    ---
    type: Reference            # Reference | API Endpoint | Runbook | Architecture
    title: Short Title         #            | Dataset | Metric | Decision | NPC | Item …
    description: One line.
    tags: [a, b]
    resource: <uri or repo path>   # optional — what the concept points at
    source: <origin url>           # optional — provenance for references
    timestamp: 2026-06-21
    ---

    # Title
    Body. Link with [[other-slug]].
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

import yaml

_FRONTMATTER = re.compile(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", re.DOTALL)
_LINK = re.compile(r"\[\[([a-z0-9][a-z0-9\-/]*)\]\]")
_CODE_FENCE = re.compile(r"```.*?```", re.DOTALL)
_INLINE_CODE = re.compile(r"`[^`]*`")

REQUIRED_FIELDS = ("type", "title", "description")


def _extract_links(body: str) -> list[str]:
    """Find [[slug]] links, ignoring those inside code blocks / inline code
    (so a concept can *document* the link syntax without it counting as a link)."""
    stripped = _CODE_FENCE.sub(" ", body)
    stripped = _INLINE_CODE.sub(" ", stripped)
    return sorted(set(_LINK.findall(stripped)))


@dataclass
class Concept:
    """A single OKFS knowledge concept."""

    slug: str
    type: str = ""
    title: str = ""
    description: str = ""
    body: str = ""
    tags: list[str] = field(default_factory=list)
    resource: str = ""
    source: str = ""
    timestamp: str = ""
    links: list[str] = field(default_factory=list)
    path: Optional[Path] = None
    frontmatter: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_text(cls, slug: str, text: str, *, path: Optional[Path] = None) -> "Concept":
        text = text.lstrip("﻿")
        m = _FRONTMATTER.match(text)
        if not m:
            return cls(slug=slug, title=slug, body=text.strip(), path=path)
        fm = yaml.safe_load(m.group(1)) or {}
        if not isinstance(fm, dict):
            fm = {}
        body = m.group(2).strip()
        links = _extract_links(body)
        return cls(
            slug=slug,
            type=str(fm.get("type", "")),
            title=str(fm.get("title", slug)),
            description=str(fm.get("description", "")),
            body=body,
            tags=[str(t) for t in (fm.get("tags") or [])],
            resource=str(fm.get("resource", "")),
            source=str(fm.get("source", "")),
            timestamp=str(fm.get("timestamp", "")),
            links=links,
            path=path,
            frontmatter=fm,
        )

    @classmethod
    def from_file(cls, path: Path | str) -> "Concept":
        p = Path(path)
        return cls.from_text(p.stem, p.read_text(encoding="utf-8"), path=p)

    def missing_fields(self) -> list[str]:
        return [f for f in REQUIRED_FIELDS if not getattr(self, f)]

    def to_dict(self, *, include_body: bool = False) -> dict[str, Any]:
        data = {
            "slug": self.slug,
            "type": self.type,
            "title": self.title,
            "description": self.description,
            "tags": list(self.tags),
            "resource": self.resource,
            "source": self.source,
            "timestamp": self.timestamp,
            "links": list(self.links),
        }
        if include_body:
            data["body"] = self.body
        return data
