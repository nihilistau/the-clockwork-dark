---
type: Reference
title: Agent Architecture — the Two Powers
description: The engine's AI layer in depth — the Storyteller (big model, gated, evaluated) and the unreliable Assistant + Director (small model, agency-scored).
tags: [agents, storyteller, assistant, evaluator, governance, llm]
resource: engine/agents/storyteller.py
timestamp: 2026-06-21
---

# Agent Architecture — the Two Powers

Two intelligences run over the engine. Neither owns mechanical truth (that is the
hard engine in [[clockwork-engine]]); both are reined by interceptors and the
Evaluator. In-world they are [[the-two-powers]].

## The Storyteller (the Driver)

`StorytellerAgent` (`clockwork_storyteller`, the "big" profile) narrates the
world and drives the slow dark. Each turn:

- **Prompt shaping** — `_build_messages` runs governance PRE, then optional
  structured output (`STORYTELLER_RESPONSE_FORMAT`, when `lmstudio.structured_output`).
- **Streaming gate** — narration prose streams live via `ProseStreamGate`; the
  trailing fenced-json epilogue is withheld from the client.
- **Required `@skill` tools** — parsed `tool_calls` execute through
  `execute_tool_calls`; `auto_resolve_skill_check` fills in a requested roll.
- **Evaluator gate + retry** — `StorytellerEvaluator` scores tone/lore/mechanics/
  length/json/choices. A mechanical claim with no matching receipt scores 0 and
  forces one retry (`MAX_RETRIES = 1`) with `evaluator_retry_prompt` notes.
- **Resilience/budget** — `retry_call` retries flaky inference with backoff;
  `TurnBudget` (token + wall-clock ceiling) stops pathological retry loops.

## The Assistant + AssistantDirector

`AssistantAgent` (`clockwork_assistant`, the "small" profile) is the fond,
unreliable companion — indifferent-god tone, never owed. Each turn
`AssistantDirector.decide` scores agency from `help_probability` plus *struggle*
(low HP, combat, low stamina) and *drama* (evil phase, dramatic beats), minus a
recent-appearance cooldown:

- **appear** — one rng draw vs the score (a calm turn matches the legacy
  `should_assistant_speak`); at real danger a floor of 0.9 makes it show up.
- **intent** — `quip | hint | lore | warning | gift`, chosen from struggle,
  trust, and awareness.
- **reliability** — `0.45 + 0.5*trust`; on a low roll its advice may mislead.
- **gift** — the right item at the right moment (`assistant_gift` skill,
  engine-granted, on a cooldown).

## How they are steered and reined

PRE interceptors and decorators *steer* (tone, GM disposition, agency knobs in
`AgentMind`); the engine and POST `RulesGovernor` *rein in* (every number comes
from a skill receipt; overreach is recorded, not honored). Transport is
provider-agnostic ([[lmstudio-integration-overview]]); the tightening toward
native tool-calls is [[llm-migration-plan]].
