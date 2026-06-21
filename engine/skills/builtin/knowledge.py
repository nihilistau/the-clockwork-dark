"""
Knowledge Skills (PR22)
=======================

Let the agents read the OKFS knowledge bundle at runtime — search by query,
then pull a single concept's body for progressive disclosure.
"""

from __future__ import annotations

import json

from engine.okfs import get_bundle
from engine.skills.registry import skill


@skill(
    pack="clockwork",
    description=(
        "Search the OKFS knowledge base (lore, design, references). Returns the "
        "top matching concepts as {slug, title, type, description}."
    ),
    category="NARRATIVE",
    trigger="optional",
)
def query_knowledge(query: str, limit: int = 3) -> str:
    """Term-overlap search over the knowledge bundle."""
    bundle = get_bundle()
    hits = bundle.search(query, limit=int(limit))
    return json.dumps(
        {
            "query": query,
            "results": [
                {
                    "slug": c.slug,
                    "title": c.title,
                    "type": c.type,
                    "description": c.description,
                }
                for c in hits
            ],
        }
    )


@skill(
    pack="clockwork",
    description="Read one OKFS concept's full body by slug (progressive disclosure).",
    category="NARRATIVE",
    trigger="optional",
)
def read_concept(slug: str) -> str:
    """Return a single concept body + its outbound links."""
    bundle = get_bundle()
    concept = bundle.get(slug)
    if concept is None:
        return json.dumps({"error": f"No concept: {slug}"})
    return json.dumps(
        {
            "slug": concept.slug,
            "title": concept.title,
            "type": concept.type,
            "body": concept.body,
            "links": concept.links,
        }
    )
