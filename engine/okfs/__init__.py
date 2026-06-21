"""
OKFS — our in-repo Open Knowledge Format (PR22)
===============================================

One concept per Markdown file (YAML frontmatter + body + ``[[slug]]`` links),
loaded into a queryable, validatable knowledge graph. Provider-agnostic and
zero-runtime-lock-in: it's just text the agents (and humans) traverse.
"""

from engine.okfs.bundle import OKFSBundle, get_bundle, reset_bundle
from engine.okfs.concept import Concept

__all__ = ["Concept", "OKFSBundle", "get_bundle", "reset_bundle"]
