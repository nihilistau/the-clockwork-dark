---
type: Agent Guide
title: AGENTS.md — Working in The Clockwork Dark
description: Vendor-neutral guide for any AI agent — read/extend the OKFS knowledge system, honor the engine.
tags: [agent-guide, agents, okfs, onboarding]
resource: knowledge/index.md
timestamp: 2026-06-21
---

# AGENTS.md — Working in The Clockwork Dark

Any agent (Claude, Codex, local models, future tooling) works the same way here:
**the project's knowledge lives in OKFS**, and so do these instructions. (Why:
[[okfs-conventions]].)

## OKFS in 30 seconds
One concept = one Markdown file with YAML frontmatter (`type`, `title`,
`description` required) + body + `[[slug]]` links. Git-native, agent-traversable,
zero runtime lock-in. Spec + tooling: [[okfs-spec]]. Root: `knowledge/index.md`.

This repo is **more than one game**: a reusable engine ([[clockwork-engine]]) you
can retarget to a new story ([[building-on-the-engine]]). The catalogue of systems
is [[systems-catalog]]; to add one, [[extending-the-engine]].

## Your loop
1. **Orient** — read `knowledge/index.md`, follow the links your task needs
   (progressive disclosure: read three small files, not three thousand lines).
2. **Act** — the engine owns mechanics; you propose, it resolves. Config-first
   (`get_config()`), reuse before rewrite, keep `pytest` green.
3. **Record** — capture durable findings as new concepts (`knowledge/<area>/<slug>.md`);
   run `OKFSBundle.validate()` (no missing frontmatter, no broken links), refresh the
   index (`python scripts/build_okfs_index.py`), and log notable changes in [[changelog]].

## Programmatic access
- Python: `from engine.okfs import get_bundle; get_bundle().search("...")`.
- In-game agents: the `query_knowledge` and `read_concept` `@skill` tools.

## Provider-agnostic
We speak to the LLM over the OpenAI-compatible REST API
([[lmstudio-integration-overview]]); LM Studio is today's backend, not a
dependency ([[llm-migration-plan]]). Same for images/voice
([[install-comfyui]], [[install-voxtral]], [[run-on-the-beast]]).

Claude Code specifics: `CLAUDE.md`. A drop-in onboarding prompt: `prompt.md`.
