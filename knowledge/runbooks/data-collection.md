---
type: Runbook
title: Turn Data Collection (self-improvement)
description: Capture each turn to JSONL for future fine-tuning, and schedule maintenance cadence deterministically.
tags: [runbook, training, data, fine-tuning, scheduler]
resource: engine/training/data_collector.py
timestamp: 2026-06-21
---

# Turn Data Collection (self-improvement)

The engine can record every resolved turn to a JSONL file so the system can later
be **fine-tuned on its own play**. This is self-improvement *plumbing*, not a new
authority: the collector reads a finished turn payload, writes one line, and never
touches state or the hard engine. It sits right beside the Oracle ([[turn-metrics]])
in `content/scenes/clockwork/clockwork_state.py` — gated and wrapped so it can
**never break a turn**.

## Turn it on

Collection is **off by default** (so CI and normal play write nothing). Enable it
in `config/local.yaml` (gitignored; deep-merges over `config/default.yaml`):

```yaml
training:
  collect: true                          # write one JSONL line per turn
  data_path: "data/training/turns.jsonl" # repo-relative; the dir is gitignored
```

The sink path is config-driven (never hardcoded): the collector honours
`paths.training_data` first, then `training.data_path`, then the built-in default
`data/training/turns.jsonl`. The parent directory is created on first write, and
`data/training/` is gitignored so captured play never lands in version control.

## What each line captures

One JSON object per turn, flattened for fine-tuning:

- `session_id`, `turn_number`, `player_action`
- `narration`, `choices` (count)
- `tool_receipts` — `{skill, success}` per engine receipt
- `evaluation` — `{overall, passed}` from the Evaluator
- `governance` — count of recorded violations
- `assistant` — `{spoke, intent, gift}`
- `doom` — the Doom Clock snapshot if present
- `evil_progress`, `latency_ms`, `ts`

## Maintenance cadence (Scheduler)

`engine/training/scheduler.py` is a tiny, **clock-injected** cadence runner used
for world-tick / maintenance tasks. It owns no threads and no wall clock — the
host loop calls `tick(now)` and the scheduler runs only the tasks whose interval
has elapsed, returning their names. This keeps cadence **deterministic and
unit-testable**, the same way `WorldSim.should_run_realtime_tick(now=...)` takes
an injected clock.

```python
from engine.training import Scheduler

sched = Scheduler()
sched.add_task("world_tick", 300.0, run_maintenance)
sched.tick(now=0.0)    # -> ["world_tick"]  (first run fires immediately)
sched.tick(now=120.0)  # -> []              (interval not elapsed)
sched.tick(now=300.0)  # -> ["world_tick"]  (elapsed since last run)
```

## Verify

```bash
python -m pytest tests/test_data_collector.py tests/test_scheduler.py -q
```

With `training.collect: true`, play a few turns and confirm
`data/training/turns.jsonl` grows by one line per turn. With it `false`, the file
is never written.

Related: [[turn-metrics]], [[clockwork-architecture]]
