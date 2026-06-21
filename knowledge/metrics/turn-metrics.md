---
type: Metric
title: Turn Metrics (Oracle)
description: The per-turn telemetry the Oracle aggregates and serves at /api/metrics.
tags: [metric, observability, oracle, telemetry]
resource: engine/observability/oracle.py
timestamp: 2026-06-21
---

# Turn Metrics (Oracle)

`engine/observability/oracle.py` rolls every turn payload into aggregates so the
system's health is visible at **`GET /api/metrics`** (`{ metrics, recent }`).

## Aggregates
- **turns** — total turns recorded.
- **eval_pass_rate** — fraction of turns the Storyteller Evaluator passed.
- **avg_eval** — mean Evaluator `overall` score (0–1).
- **violation_rate / violations_total** — turns with ≥1 governance (SceneRulesEngine)
  violation, and the running total.
- **assistant_intervention_rate** — fraction of turns the Assistant spoke (vs. its
  indifferent silence).
- **gifts** — count of director-driven Assistant gifts (the right item at the
  right moment).
- **avg_latency_ms** — mean wall-clock per turn (storyteller + assistant).
- **last_evil_progress** — the corruption's current drift.

## Reading them
The ring buffer keeps the last ~200 turns (`oracle.recent(n)`); aggregates are
O(1). These are the levers for tuning the "let the AI loose / rein it in" balance
([[clockwork-architecture]]): a low `eval_pass_rate` or high `violation_rate`
means the model needs tighter prompting or structured output; a runaway
`assistant_intervention_rate` means the Director is too eager.

Related: [[clockwork-architecture]]
