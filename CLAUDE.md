# CLAUDE.md — The Clockwork Dark

This file guides Claude Code (and other coding agents) when working in this repository.

## Start here

1. **Read** [docs/CLAUDE_CODE_BRIEF.md](docs/CLAUDE_CODE_BRIEF.md) — implementation spec, golden rules, PR DAG
2. **Read** [docs/DESIGN.md](docs/DESIGN.md) — vision, mechanics, glossary, architecture
3. For visual/asset work, use [docs/CLAUDE_DESIGN_BRIEF.md](docs/CLAUDE_DESIGN_BRIEF.md) instead

## Critical rules

1. **Engine resolves mechanics; LLMs narrate.** All dice, combat, inventory, and travel go through `@skill` tools.
2. **Never hardcode** ports, model names, or paths — use `config/default.yaml` via `get_config()`.
3. **Reuse patterns** from [CosySim](https://github.com/nihilistau/CosySim) and [Archives of Anubis](https://github.com/nihilistau/Achieves-Of-Anubis) before writing new code.
4. **Prove with tests** — run `pytest` before declaring work complete.
5. **Windows-aware** — LM Studio at `http://localhost:1234/v1`; use `scripts/start.ps1`.

## Project summary

Local-first AI RPG: deterministic hard engine + two autonomous agents (Storyteller + Assistant). ComfyUI images/video, local TTS/STT. Player starts at the forest edge; evil ticks in the background whether they become a hero or a baker.

## Implementation order

Follow the PR plan in DESIGN.md § PR Plan. **PR1–PR12 complete; v0.2 PR13–PR15 landed** (grounded combat, crafting/professions, Millhaven march arc + cutscene milestones). The design system is integrated and local-first (see [docs/AUDIT.md](docs/AUDIT.md)). Next candidates: Echo system / permadeath, full convergence arc, ComfyUI live rendering.

## First-session prompt

```
Read docs/CLAUDE_CODE_BRIEF.md and docs/DESIGN.md.
Implement PR1–PR3 only. Prove with pytest tests/ -v.
```

## Canon IDs (do not rename)

- Agents: `clockwork_storyteller`, `clockwork_assistant`
- Locations: `forest_clearing`, `edgewood_square`, `edgewood_bakery`, `tinker_caravan`, `millhaven_gate`
- Evil phases: `dormant`, `stirring`, `spreading`, `consuming`