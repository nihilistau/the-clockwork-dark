---
type: Agent Guide
title: CLAUDE.md — The Clockwork Dark
description: How Claude Code (and any coding agent) works in this repo, via the OKFS knowledge system.
tags: [agent-guide, claude, okfs, onboarding]
resource: knowledge/index.md
timestamp: 2026-06-21
---

# CLAUDE.md — The Clockwork Dark

This repo runs on **OKFS** — our Open Knowledge Format. Knowledge, design,
runbooks, references, and even these agent guides are one-concept Markdown files
with YAML frontmatter and `[[slug]]` links. **Read the knowledge bundle first,
then code.** (Why: [[okfs-conventions]].)

## Start here (OKFS)
1. `knowledge/index.md` — the root; follow the links.
2. [[okfs-spec]] — the format + tooling (`engine/okfs/`, `query_knowledge` / `read_concept` skills).
3. [[clockwork-architecture]] — what we're building.
4. [[lmstudio-integration-overview]] + [[llm-migration-plan]] — the LLM layer.
5. Long-form specs: `docs/CLAUDE_CODE_BRIEF.md`, `docs/DESIGN.md`, `docs/AUDIT.md`.

## Use OKFS as you work
- **Read it:** `from engine.okfs import get_bundle` (or, in-game, the `query_knowledge` /
  `read_concept` skills).
- **Extend it:** add `knowledge/<area>/<slug>.md` with required frontmatter
  (`type`, `title`, `description`); link related concepts with `[[slug]]`; keep it
  atomic (one idea per file).
- **Validate it:** `OKFSBundle.validate()` and `tests/test_okfs.py` fail on missing
  frontmatter or broken links — keep the bundle green.

## Critical rules
1. **Engine resolves mechanics; LLMs narrate.** Dice / combat / craft / inventory /
   travel go through `@skill` tools; governance audits the rest ([[clockwork-architecture]]).
2. **Never hardcode** ports / models / paths — use `get_config()` (`config/default.yaml`,
   overridden by gitignored `config/local.yaml`; see [[run-on-the-beast]]).
3. **Reuse patterns** from CosySim and Archives of Anubis before writing new code.
4. **Prove with tests** — `pytest` green before declaring done.
5. **Windows-aware** — PowerShell; LM Studio at `lmstudio.base_url`; `scripts/start.ps1`.
6. **Knowledge is OKFS** — capture durable knowledge as a concept, not a code comment.

## Status
Local-first AI RPG: deterministic engine + Storyteller/Assistant agents, OKFS
knowledge, ComfyUI images + Voxtral voice. **PR1–PR25 landed (v0.5):** live LLM loop
hardened (streaming, structured output, resilience), governance pipeline +
SceneRulesEngine wired, OKFS backbone, ComfyUI/Voxtral setup. Next: Phase 5 (depth —
the unreliable Assistant Director, systems, story arcs) and Phase 6 (observability).

## Canon IDs (do not rename)
- Agents: `clockwork_storyteller`, `clockwork_assistant`
- Locations: `forest_clearing`, `edgewood_square`, `edgewood_bakery`, `tinker_caravan`, `millhaven_gate`
- Evil phases: `dormant`, `stirring`, `spreading`, `consuming`

For non-Claude agents see `AGENTS.md`; for a drop-in onboarding prompt see `prompt.md`.
