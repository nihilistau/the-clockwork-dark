---
type: Prompt
title: Agent Onboarding Prompt — The Clockwork Dark
description: A drop-in system/first-message prompt that points any agent at the OKFS knowledge system.
tags: [prompt, onboarding, okfs, agents]
resource: AGENTS.md
timestamp: 2026-06-21
---

# Agent Onboarding Prompt

Use the block below as a system or first-message prompt when starting an agent on
this repository. (It mirrors `AGENTS.md`; the why is [[okfs-conventions]].)

---
You are working on **The Clockwork Dark**, a local-first AI RPG. The project's
knowledge lives in **OKFS** — one-concept Markdown files with YAML frontmatter and
`[[slug]]` links, under `knowledge/`.

Before you code:
1. Read `knowledge/index.md` and follow the links relevant to your task.
2. Skim [[okfs-spec]] (the format) and [[clockwork-architecture]] (the system).
3. Honor the project rules (CLAUDE.md / AGENTS.md): the **engine resolves all
   mechanics — LLMs only narrate**; never hardcode ports/models/paths (use
   `get_config()`); reuse before rewriting; keep `pytest` green; and capture any
   durable knowledge you produce as a new OKFS concept, keeping the bundle valid
   (`OKFSBundle.validate()`).

Query the knowledge base in code with `engine.okfs.get_bundle()`, or in-game via
the `query_knowledge` / `read_concept` skills. Work in small, tested increments.
---
