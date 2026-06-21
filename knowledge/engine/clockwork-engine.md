---
type: Architecture
title: The Clockwork Engine
description: The reusable three-layer engine beneath The Clockwork Dark — a deterministic hard core, two autonomous LLM agents, and a governance pipeline.
tags: [architecture, engine, agents, governance, reusable]
resource: engine/game/engine.py
timestamp: 2026-06-21
---

# The Clockwork Engine

The Clockwork Dark is one *game*; underneath it is a general **engine** for
LLM-driven RPGs. The shape, in one breath: a deterministic core holds all
mechanical truth, two autonomous agents improvise on top, and a governance layer
reins them in. Swap the content and the same engine runs a different story — see
[[building-on-the-engine]].

## Three layers

1. **Deterministic hard engine** (`engine/game/`) — the only authority over
   dice (`dice.py`), combat (`combat.py`), crafting (`crafting.py`), travel,
   challenges (`challenges.py`), contracts (`contracts.py`), and the background
   evil/Doom Clock (`evil_ticker.py`, `doom_clock.py`). All state lives in
   `GameState`; `GameEngine` is the sole mutator. The LLM never touches state
   directly — it calls `@skill` tools (`engine/skills/`), many marked
   `TRIGGER_REQUIRED` (`roll_dice`, `resolve_skill_check`, `move_to`,
   `resolve_combat`, `query_evil_state`). The model may *propose*; the engine
   *decides*.
2. **Two autonomous agents** (`engine/agents/`) — the Storyteller (the Driver)
   and the unreliable Assistant. Detailed in [[agent-architecture]].
3. **Governance** (`engine/governance/`) — a priority-ordered PRE/POST
   interceptor pipeline wrapped around every turn, finished by the
   `SceneRulesEngine` (R001–R005).

## How a turn flows

A player choice enters `StorytellerAgent.run_turn`. `_build_messages` composes
the system prompt, then **governance PRE** interceptors shape it
(`EvilPhaseTone`, `DoomBeatInterceptor`, `StorytellerMind`, lore/awareness
gating) in priority order. The LLM **streams** prose through a `ProseStreamGate`
that withholds the JSON epilogue. The parsed `tool_calls` are **resolved** by the
engine (real receipts, real math). The **Evaluator** scores the turn on a
6-point rubric; if it claims mechanics without a receipt, it fails and the turn
**retries** with notes (bounded by `TurnBudget` and `retry_call` backoff from
`resilience.py`). On success, **governance POST** audits the resolved state via
`RulesGovernor` (awareness clamp, evil never decreases, canonical location,
stat-delta overreach — all recorded). The world tick advances the evil ticker;
the **Doom Clock** surfaces any newly-crossed beats; media fires from tags.

The balance: let the AIs surprise; let the engine keep them fair. See
[[clockwork-architecture]] for the project view and [[systems-catalog]] for the
full system list.
