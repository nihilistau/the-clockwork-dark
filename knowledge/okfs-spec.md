---
type: Reference
title: OKFS — Our Open Knowledge Format
description: The one-concept-per-file Markdown+frontmatter format this bundle uses.
tags: [okfs, spec, knowledge, format]
resource: engine/okfs/concept.py
timestamp: 2026-06-21
---

# OKFS — Our Open Knowledge Format

OKFS is our in-repo take on the Open Knowledge Format: **one concept per Markdown
file**, git-native, agent-traversable, with zero runtime lock-in (it's just UTF-8
text). It backs documents, lore, NPCs, items, runbooks, metrics, API docs,
datasets and tables — anywhere structured, linkable knowledge helps.

## File shape
```
---
type: Reference            # Reference | API Endpoint | Runbook | Architecture
title: Short Title         #            | Dataset | Metric | Decision | NPC | Item | Location …
description: One line used for relevance ranking.
tags: [a, b]
resource: <uri or repo path>   # optional — what the concept points at
source: <origin url>           # optional — provenance for reference docs
timestamp: 2026-06-21
---

# Title
Body in Markdown. Link related concepts with [[other-slug]].
```

## Rules
- **Required frontmatter:** `type`, `title`, `description`. The rest are optional.
- **Slug** = the filename stem (kebab-case). Links use `[[slug]]`.
- **Links must resolve** to a concept in the bundle (the validator fails on broken links).
- **Atomic:** one idea per file; split rather than nest.

## Tooling
`engine/okfs/` loads a directory tree into an `OKFSBundle`: lookup by slug,
filter `by_type`/`by_tag`, follow `neighbors` (linked concepts), `search` by
term overlap, and `validate` (missing fields + broken links). `get_bundle()`
returns the process-wide bundle rooted at `paths.knowledge`.

See [[clockwork-architecture]] for how this fits the wider system.
