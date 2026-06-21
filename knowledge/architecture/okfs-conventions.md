---
type: Decision
title: OKFS Everywhere — Convention
description: Why all project knowledge AND the agent guides (CLAUDE.md, AGENTS.md, prompt.md) use OKFS.
tags: [okfs, convention, decision, agents, docs]
resource: knowledge/okfs-spec.md
timestamp: 2026-06-21
---

# OKFS Everywhere — Convention

**Decision:** every durable document in this project uses [[okfs-spec]] — not only
the `knowledge/` bundle, but the agent guides at the repo root (`CLAUDE.md`,
`AGENTS.md`, `prompt.md`) too.

## Why
- **One system to learn.** An agent that understands OKFS understands all our docs.
- **Traversable.** Frontmatter + `[[links]]` let agents and humans jump straight to
  the relevant concept instead of reading everything.
- **Git-native, zero lock-in.** Plain UTF-8 Markdown; diffs, branches, and PRs all
  work; no database or SDK required.
- **Self-documenting graph.** `engine/okfs/` loads + validates the bundle, and the
  same format powers the in-game `query_knowledge` / `read_concept` skills.

## Rules
- New durable knowledge → a concept in `knowledge/<area>/<slug>.md` (required
  frontmatter `type` / `title` / `description`; atomic; link with `[[slug]]`).
- The root agent guides use the same frontmatter + links but live at the repo root
  so tools find them; they point *into* the bundle and are not loaded as bundle
  concepts (so their links aren't validated — keep them accurate by hand).
- Keep it green: `OKFSBundle.validate()` (`tests/test_okfs.py`) must pass — no
  missing fields, no broken links inside the bundle.

Start at `knowledge/index.md`.
