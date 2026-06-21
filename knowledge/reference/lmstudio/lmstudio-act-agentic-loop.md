---
type: Reference
title: The .act() Agentic Run-Until-Done Loop
description: LM Studio's multi-round tool-calling API that drives a model until it returns a final answer.
tags: [lmstudio, python-sdk, agent, tool-calling]
source: https://lmstudio.ai/docs/python/agent/act
timestamp: 2026-06-21
---

# The .act() Agentic Run-Until-Done Loop

`model.act()` is LM Studio's **automatic multi-round tool-calling** API. A "round" is: model emits a tool call -> SDK runs the tool -> result is fed back -> model decides again — looping until the model produces a final answer (no further tool calls). This automates what we otherwise orchestrate by hand.

Shape:
```python
model.act(
    "Your prompt or Chat object",
    [tool_fn_1, tool_fn_2],
    on_message=callback,
    on_prediction_fragment=callback,
)
```
Key arguments: a prompt/`Chat`, a list of tools, and callbacks — `on_message` (fires with the assistant message per completed round and with each tool-result message; intended for appending to chat history, gets no round index), `on_prediction_fragment` (streaming text fragments, with round index), plus `on_round_start`/`on_round_end`/`on_prediction_completed` lifecycle hooks and `handle_invalid_tool_request`. `max_parallel_tool_calls` controls concurrency (default 1); a round/iteration cap likely exists (e.g. `max_prediction_rounds`) — verify against SDK. Gotcha: tool-use quality is model-dependent ("bigger is better"; Qwen2.5-7B-Instruct recommended as a baseline).

**How The Clockwork Dark applies this:** `.act()` is conceptually exactly our agent loop — narrate, call a skill, feed the result, continue — but baked into the SDK. Since we stay provider-agnostic over the OpenAI-compatible REST API, we implement our *own* `.act()`-style loop and reuse its round/callback model as a design template: `on_prediction_fragment` maps to our streaming gate, `on_round_start/end` are natural governance checkpoints (budget, evil-tick cadence, safety), and a round cap guards runaways. We keep both Storyteller and Assistant on this hand-driven loop so behavior is deterministic and testable, treating LM Studio's `.act()` as a reference design rather than a runtime dependency.

Related: [[lmstudio-python-agent-tools]], [[lmstudio-mcp-host]]
