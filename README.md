# The Clockwork Dark

A local-first AI roleplaying game where a deterministic engine holds truth and two autonomous LLM agents — the **Storyteller** and the **Assistant** — narrate a living frontier world. ComfyUI generates scene images and cutscenes; local TTS/STT handles voice.

You can become a baker in Edgewood and never learn the clock is ticking. Or you can march inward toward the Heartlands until the **Clockwork Dark** can no longer be ignored.

## Documentation

| Document | Audience | Purpose |
|----------|----------|---------|
| [docs/DESIGN.md](docs/DESIGN.md) | Architects, you | Full system design, story bible, mechanics, PR plan |
| [docs/CLAUDE_DESIGN_BRIEF.md](docs/CLAUDE_DESIGN_BRIEF.md) | Claude Design | Art direction, UI, ComfyUI prompts, audio |
| [docs/CLAUDE_CODE_BRIEF.md](docs/CLAUDE_CODE_BRIEF.md) | Claude Code / agents | Build spec, borrow map, APIs, task DAG |
| [CLAUDE.md](CLAUDE.md) | Coding agents | Quick onboarding pointer |

## Parent projects

Built by merging patterns from:

- [Archives of Anubis](https://github.com/nihilistau/Achieves-Of-Anubis) — hard engine + narrative council + RAG lore
- [CosySim](https://github.com/nihilistau/CosySim) — AgentGovernor, `@skill` tools, SSE tags, dual-agent scenes

## Status

**v0.1 — design phase complete.** Implementation follows the 12-PR plan in `docs/DESIGN.md`.

## Quick start (after implementation)

```powershell
# Prerequisites: Python 3.13, LM Studio on :1234
pip install -r requirements.txt
.\scripts\start.ps1
# Open http://localhost:5573
```