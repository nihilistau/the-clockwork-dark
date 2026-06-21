---
type: Log
title: Changelog — The Clockwork Engine
description: A running, append-only log of meaningful changes — OKFS used on ourselves.
tags: [log, changelog, okfs, history]
resource: knowledge/_index.json
timestamp: 2026-06-21
---

# Changelog — The Clockwork Engine

We keep this as a live example: OKFS used *on ourselves*. Append newest at top.
Each entry is a date, a one-line summary, and the OKFS `bundle_hash` after the
change (see [[okfs-spec]] and `knowledge/_index.json`).

## 2026-06-22 — behavioural smoke + CI
- **jsdom dialog tests** — the a11y dialog manager is extracted to
  `clockwork-dialogs.js` (a `create(doc)` factory) and behaviourally tested under
  jsdom: open/focus-in, Escape-to-close + focus-restore, stacking, Tab focus-trap
  (7 tests). `clockwork.js` consumes it via `window.ClockworkDialogs`.
- **Playwright e2e smoke** — `frontend-tests/e2e/` has Playwright boot the Flask
  server itself (no LLM) and smoke the real page: helper/dialog modules wired,
  zero console errors, a dialog opens and Escape dismisses it.
- **CI** — `.github/workflows/ci.yml` runs three jobs on every push/PR: pytest
  (359), vitest + jsdom (18), and the Playwright chromium smoke.

## 2026-06-22 — audit follow-ups (a11y · frontend harness · test gaps)
The deferred items from the review, plus a real bug the new tests surfaced:
- **Accessibility** — all four `role="dialog"` overlays now have Escape-to-close,
  focus-trap, focus-on-open, and focus-restore; the doom-end modal got a dismiss
  button; global `:focus-visible` + a `prefers-reduced-motion` block; the dead
  mic button is disabled; ambient toasts are `polite`, not `assertive`.
- **Frontend test harness** — pure helpers (`escapeHtml`, `challengeView`)
  extracted to `clockwork-helpers.js`; a vitest project under `frontend-tests/`
  (11 tests) unit-tests them, and `tests/test_frontend_contract.py` (8) locks the
  a11y/XSS invariants from the Python suite with no Node needed.
- **Backend test gaps** — +32 tests: governance through the real turn (R003 in the
  payload), `chat_stream` error/timeout → fallback, the **consumed** finale,
  contract double-complete/accept guards, challenge branch/failure paths, socket
  `narration_delta`/`error`.
- **Engine fix** — `tool_dispatcher.execute_tool` was laundering a *rejected*
  required action (an illegal `move_to`) into a `success: True` receipt, so the
  Evaluator's failed-required-tool gate never fired; now an explicit
  `success: False` counts as a failure (dice resolvers excluded, where `success`
  is the roll outcome).
- **359 tests passing.**

## 2026-06-22 — review & audit tighten
A full five-dimension review (correctness · security · architecture · tests ·
docs), every finding verified in code. No critical defects; the fixes are
tightenings (full report in `docs/AUDIT.md`):
- **Security** — default bind is now `127.0.0.1` (was `0.0.0.0`), Socket.IO CORS
  is a localhost allow-list (was `*`), and a `MAX_CONTENT_LENGTH` upload cap —
  all under a new `security:` config block; LAN exposure is now opt-in.
- **Robust Assistant parsing** — the Assistant shares the Storyteller's
  balanced-brace extractor (`engine/agents/parsing.py`) instead of a brittle
  regex that truncated nested objects.
- **Frontend XSS** — model-controlled strings (item names, rumors, foe text) now
  pass through `escapeHtml`.
- **Save symmetry** — `to_dict`/`from_dict` round-trip the agent minds via an
  explicit `include_minds` flag (default payload stays client-safe).
- **Hardening + DRY** — AI challenge specs are size-bounded; `_add_item` is
  unified in `engine/game/inventory.py`; README test count refreshed (318).
- Locked by `tests/test_audit_tighten.py`; **327 tests passing.**

## 2026-06-22 — the four-stream fleet
A documentation/feature fleet shipped four streams in parallel, merged in sequence:
- **Prove the engine** — *The Drowned Carillon*, a second story under `games/drowned-carillon/`
  (its own OKFS sub-bundle + data), reusing the engine with zero edits ([[building-on-the-engine]]).
- **Bespoke UI** — the doom gauge, beat toasts, end-state, the challenge overlay, the
  contract slate, and Assistant gift/intent cues, on the candlelit design tokens.
- **More world** — chance encounters on travel, the convergence finale + reckoning,
  the tinker's questline, and deeper lore ([[the-heartlands]], [[the-tinkers]],
  [[beneath-the-tunnels]], [[sympathy-and-naming]], [[the-convergence]]).
- **Self-improvement** — the DataCollector (JSONL turn capture → fine-tuning, gated off)
  and a testable Scheduler ([[data-collection]]).
- **318 tests passing.**

## 2026-06-21 — world expansion
- **Chance encounters on travel** — a new seeded, deterministic `engine/game/encounters.py`
  rolls once on arrival from the destination edge's `danger_dc` and the evil phase,
  yielding `none` (calm by default), a harmless `discovery` (engine-granted reward),
  or an `ambush` that names a `clockwork`-tagged foe the Storyteller may fight. One
  backward-compatible hook in `GameEngine.move_to` (`MoveResult.encounter`, default
  None); tunables under config `encounters:` and `data/encounters.yaml`; read-only
  skill `query_encounter_foes`.
- **The convergence finale** — the Doom Clock gains a `Convergence` layer: the
  approach to the clockwork tower as ordered reckoning beats (reusing `cutscene_tower`
  / `cutscene_consuming_horizon`) and the player's **last engine-resolved choice**
  (`stand` / `unmake` / `walk_away`), adjudicated on d20 + engagement vs a
  progress-scaled DC. Holding the line ends the game un-consumed; the `consumed`
  terminal is untouched. Skills `query_convergence`, `resolve_reckoning`. New lore
  [[the-convergence]].
- **The Tinker's Reckoning** — a four-step Ilya-the-tinker (the Assistant's face)
  contract chain appended to `data/contracts.yaml`, gated by awareness/phase, with
  engine-granted rewards ending in a sympathy lamp + engagement. New lore
  [[the-tinkers-questline]], [[the-tinkers]].
- **Deeper lore** — [[the-heartlands]], [[beneath-the-tunnels]], [[sympathy-and-naming]]
  join the above; existing concepts cross-linked; the index's lore section regrouped.

## 2026-06-21
- **Self-improvement plumbing** — a `DataCollector` (`engine/training/`) captures each
  resolved turn to JSONL for future fine-tuning (gated by `training.collect`, off by
  default; sink `data/training/` is gitignored), wired beside the Oracle in `run_turn`
  so it never breaks a turn; plus a deterministic, clock-injected `Scheduler` for
  world-tick / maintenance cadence. New runbook [[data-collection]].
- **It's an engine** — reframed as a reusable engine, not just one game. New engine
  concepts [[clockwork-engine]], [[agent-architecture]], [[building-on-the-engine]],
  [[systems-catalog]], [[extending-the-engine]]; a comprehensive `README.md` (assets,
  diagram, systems, OKFS-as-engine); agent guides updated to the index/changelog
  workflow. Authored by a documentation fleet.
- **OKFS hashing + index** — every concept now carries a content hash; the bundle
  a roll-up hash. `scripts/build_okfs_index.py` writes the lockfile
  `knowledge/_index.json`; a test fails if it goes stale. This changelog added.
- **The soul shipped** — Doom Clock ([[doom-arcs]], [[the-harvest]]), the unreliable
  Assistant Director, ephemeral [[ephemeral-challenges]] challenges, and the
  [[the-notice-board]] contracts. The two powers: [[the-two-powers]].
- **Foundations** — live LLM loop hardened (streaming, [[lmstudio-structured-output]],
  resilience), governance pipeline wiring SceneRulesEngine, OKFS knowledge backbone,
  ComfyUI/Voxtral setup ([[install-comfyui]], [[install-voxtral]], [[run-on-the-beast]]).
- **Observability** — the Oracle ([[turn-metrics]]) for pacing.

See [[clockwork-architecture]] for the system and [[okfs-conventions]] for why
everything — including this log — is OKFS.
