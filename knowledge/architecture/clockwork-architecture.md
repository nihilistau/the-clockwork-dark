---
type: Architecture
title: The Clockwork Dark — System Architecture
description: What we're building — a deterministic engine reined over two autonomous LLM agents.
tags: [architecture, clockwork, agents, engine, governance]
resource: docs/DESIGN.md
timestamp: 2026-06-21
---

# The Clockwork Dark — System Architecture

A local-first, gloomy-but-elegant AI RPG. The shape, in one breath: **a
deterministic engine holds all mechanical truth; two autonomous LLM agents
improvise on top; a governance layer reins them in.**

## The three layers
1. **Hard engine** (`engine/game/`) — the only authority over dice, combat,
   crafting, inventory, travel, evil-phase and awareness. State lives in
   `GameState`; mechanics flow exclusively through the `@skill` registry
   (`engine/skills/`). The LLM may *propose*, never *decide*.
2. **The two agents** (`engine/agents/`) —
   - **Storyteller** (`clockwork_storyteller`, "big" model): drives world and
     story, calls required skills, streams prose (epilogue withheld by
     `ProseStreamGate`), passes an Evaluator quality gate with retry.
   - **Assistant** (`clockwork_assistant`, "small" model): the *unreliable*
     companion — helps, is indifferent, or shows up at the right beat with the
     right word or item. Its agency is a deliberate dial, not a bug.
3. **Governance** (`engine/governance/`) — a priority-ordered PRE/POST
   interceptor pipeline around every turn. PRE shapes the prompt (lore, tone,
   agency, spoiler-gating); POST audits the result via the `SceneRulesEngine`
   (R001–R005), recording any LLM overreach.

## Supporting systems
- **Knowledge:** this OKFS bundle ([[okfs-spec]]) — lore, NPCs, items, runbooks,
  metrics, API docs — queried by the agents.
- **Media:** ComfyUI images + Voxtral voice, config-driven (local **or** the
  networked "beast"), degrading gracefully to placeholders/text.
- **LLM transport:** a provider-agnostic OpenAI-compatible client
  ([[lmstudio-integration-overview]]); LM Studio is today's backend, not a
  dependency.

## The balance we're chasing
Let the AIs run loose enough to surprise; rein them with the engine + governance
enough to stay coherent and fair. The migration toward native structured output
and tool-calls ([[llm-migration-plan]]) tightens that loop further.
