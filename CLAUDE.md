---
type: Agent Guide
title: CLAUDE.md — The Clockwork Dark
description: How Claude Code (and any coding agent) works in this repo, via the OKFS knowledge system.
tags: [agent-guide, claude, okfs, onboarding]
resource: knowledge/index.md
timestamp: 2026-06-22
---

# CLAUDE.md — The Clockwork Dark

This repo runs on **OKFS** — our Open Knowledge Format. Knowledge, design,
runbooks, references, and even these agent guides are one-concept Markdown files
with YAML frontmatter and `[[slug]]` links. **Read the knowledge bundle first,
then code.** (Why: [[okfs-conventions]].)

## Start here (OKFS)
1. `knowledge/index.md` — the root; follow the links.
2. [[okfs-spec]] — the format + tooling (`engine/okfs/`, `query_knowledge` / `read_concept` skills).
3. [[clockwork-architecture]] — what we're building (project view).
4. The engine (more than this one game): [[clockwork-engine]], [[agent-architecture]], [[building-on-the-engine]], [[systems-catalog]], [[extending-the-engine]].
5. [[lmstudio-integration-overview]] + [[llm-migration-plan]] — the LLM layer.
6. Long-form specs: `docs/CLAUDE_CODE_BRIEF.md`, `docs/DESIGN.md`, `docs/AUDIT.md`.

## Use OKFS as you work
- **Read it:** `from engine.okfs import get_bundle` (or, in-game, the `query_knowledge` /
  `read_concept` skills).
- **Extend it:** add `knowledge/<area>/<slug>.md` with required frontmatter
  (`type`, `title`, `description`); link related concepts with `[[slug]]`; keep it
  atomic (one idea per file).
- **Validate it:** `OKFSBundle.validate()` and `tests/test_okfs.py` fail on missing
  frontmatter or broken links — keep the bundle green.
- **Index it:** after editing concepts run `python scripts/build_okfs_index.py`
  (refreshes the content-hashed `knowledge/_index.json`; `tests/test_okfs_index.py`
  fails if it's stale), and note meaningful changes in [[changelog]].

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
knowledge (48 concepts), ComfyUI images + Voxtral voice. **PR1–PR35 landed (v0.9):**
live LLM loop hardened, governance pipeline, the reactive world (Doom beats reshape
the map — flags, discoveries, NPC moves), set-pieces (tunnel-mouth + warden barrow),
the Forge, the convergence finale, world map, cutscenes + dice faces, reactive notice
board, frontend a11y, CI pipeline (pytest 393 + vitest 19 + Playwright e2e).
Next: live LLM playtest on the beast.

## Canon IDs (do not rename)
- Agents: `clockwork_storyteller`, `clockwork_assistant`
- Locations: `forest_clearing`, `edgewood_square`, `edgewood_bakery`, `edgewood_forge`, `tinker_caravan`, `millhaven_gate`
- Evil phases: `dormant`, `stirring`, `spreading`, `consuming`

For non-Claude agents see `AGENTS.md`; for a drop-in onboarding prompt see `prompt.md`.
