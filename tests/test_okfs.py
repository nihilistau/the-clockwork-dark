"""OKFS concept parsing, bundle loading, validation, and skills (PR22)."""

from __future__ import annotations

import json

from engine.okfs import Concept, get_bundle, reset_bundle
from engine.skills.registry import SKILL_REGISTRY
import engine.skills.builtin.knowledge  # noqa: F401 (register skills)


def test_concept_parses_frontmatter_body_and_links():
    text = (
        "---\n"
        "type: Reference\n"
        "title: Sample\n"
        "description: A sample concept.\n"
        "tags: [a, b]\n"
        "---\n"
        "# Sample\n\nBody links to [[other-slug]] and [[second-slug]].\n"
    )
    c = Concept.from_text("sample", text)
    assert c.type == "Reference"
    assert c.title == "Sample"
    assert c.tags == ["a", "b"]
    assert c.links == ["other-slug", "second-slug"]
    assert c.missing_fields() == []


def test_concept_without_frontmatter_is_safe():
    c = Concept.from_text("raw", "just some text")
    assert c.title == "raw"
    assert "type" in c.missing_fields()


def test_bundle_loads_knowledge():
    reset_bundle()
    bundle = get_bundle(force=True)
    assert len(bundle) >= 15  # 13 lmstudio + index + spec + 2 architecture
    assert bundle.get("okfs-spec") is not None
    assert bundle.get("lmstudio-integration-overview") is not None


def test_bundle_validates_clean():
    """The authored bundle must have required frontmatter and NO broken links."""
    reset_bundle()
    bundle = get_bundle(force=True)
    problems = bundle.validate()
    assert problems == [], f"OKFS bundle problems: {problems[:10]}"


def test_bundle_by_type_and_tag():
    bundle = get_bundle(force=True)
    assert any(c.slug == "lmstudio-tool-use" for c in bundle.by_type("API Endpoint"))
    assert any("lmstudio" in c.tags for c in bundle.by_tag("lmstudio"))


def test_bundle_search_and_neighbors():
    bundle = get_bundle(force=True)
    hits = bundle.search("structured output json schema", limit=3)
    assert any("structured" in c.slug for c in hits)
    nbrs = bundle.neighbors("lmstudio-integration-overview")
    assert any(c.slug == "lmstudio-streaming-events" for c in nbrs)


def test_query_knowledge_skill():
    payload = json.loads(SKILL_REGISTRY.invoke("query_knowledge", query="tool calling skills", limit=2))
    assert "results" in payload
    assert len(payload["results"]) <= 2


def test_read_concept_skill():
    payload = json.loads(SKILL_REGISTRY.invoke("read_concept", slug="okfs-spec"))
    assert payload["slug"] == "okfs-spec"
    assert "OKFS" in payload["body"]
