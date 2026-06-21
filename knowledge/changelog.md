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

## 2026-06-22 — the Forge
A new village location + NPC + crafting station ([[the-forge]]):
- **`edgewood_forge`** off the square (scene graph + `locations.py` meta +
  manifest art `Design_files/assets/Forge/`), kept by **Brann Holt** the
  blacksmith (a canon NPC).
- **Station-gated recipes** (`data/recipes/forge.yaml`) — *Mend a Blade*, *Reforge
  a Relic*, and the **Warded Blade** (brass filings + a sympathy charm worked into
  steel that bites clockwork): honest anti-Dark gear, craftable only at the anvil.
- The smith's counterpart to Maris: a mundane anchor — you can pass the whole story
  at the forge and never go to the tower. Tests in `tests/test_forge.py`; bundle at
  48 concepts.

## 2026-06-22 — the village empties (NPCs move with the Dark)
The `world_events` flavor is now real movement ([[the-village-empties]]):
- **`npc_moves` world-effect** (`engine/game/world_effects.py` +
  `data/world/doom_effects.yaml`) — crossing a beat relocates named villagers, and
  `npcs_at` reflects it. The vines breach → **Aldric** abandons the forest margin
  (`forest_forage` → `edgewood_square`); the tunnels open → **Greta** leaves the
  shrine for the square; the tower assembles → the gate thins (`gate_thinning`).
  Displaced villagers are marked and wear road-worn faces (`Design_files/assets/
  NPC-Move-Dark/`). **Maris does not move** — the baker keeps her oven to the last.
- Tests in `tests/test_npc_moves.py`; bundle at 47 concepts.

## 2026-06-22 — Hollow Hill, the Mage-Ruins & the older name
The tunnels now lead somewhere that matters at the end ([[the-first-warden]]):
- **`warden_barrow` set-piece** (`data/set_pieces.yaml`) — reachable once the
  hidden path opens. A branching descent into the barrow: the **First Warden
  husk** (raise a hand against it and it defends itself — force is the wrong
  tool), and a broken **solar star-chart**. Read the standing stones for the
  binding-star (the **Hollow Crown**), name it at the chart, and learn the
  **older name** — or trust the **faceless Assistant**, who points at the wrong
  star. Scene art from `Design_files/assets/Hollow-Hill-Mage-Ruins/`.
- **Convergence payoff** — learning the older name sets `knows_older_name`, which
  sharpens the **unmake** reckoning at the tower (`+doom.older_name_bonus`, default
  5): a true name cuts both ways. The barrow is where a player earns the edge that
  makes refusal at the tower more than a prayer ([[the-convergence]]).
- Hollow Hill & Mage-Ruins scene art wired into the manifest. Tests in
  `tests/test_warden_barrow.py`; bundle at 46 concepts.

## 2026-06-22 — the tunnel-mouth set-piece
The first **set-piece**: a discovery you descend into and *experience*, unlocked
when the reactive world opens the tunnels ([[the-tunnel-mouth]]).
- **`engine/game/set_pieces.py`** + `data/set_pieces.yaml` — authored, gated
  (`requires_flag: tunnels_open` / `requires_discovery: hidden_path`) challenges
  presented by the `start_set_piece` skill and resolved by the standard challenge
  engine. The tunnel-mouth is a branching `decision_tree` mapping the art: the
  brass ring, the A/B fork, the D/E/F rail junction, the G/H clockwork chamber —
  to sealed (engagement + `tunnel_sealed` + iron key), relic, collapse, lost, or
  retreat. The carved clue (*low, and with the water*) is the puzzle.
- **`_apply_effects` gains `set_flags`** so a terminal can durably seal the seam.
- **Bespoke overlay** — the challenge frame now renders per-node **scene art** and
  a **parchment riddle** (`clockwork-helpers.js` + `clockwork.css`), matching the
  tunnel UI mock; new assets served from `Design_files/assets/Tunnels/`.
- Tests in `tests/test_set_pieces.py` (+ a vitest case). Bundle at 45 concepts.

## 2026-06-22 — the reactive world
The Doom Clock's beats now **change the world** instead of only narrating it
([[the-reactive-world]]):
- **`engine/game/world_effects.py`** + `data/world/doom_effects.yaml` — crossing a
  beat applies declarative effects onto existing `GameState` fields (so they save
  for free): set flags, accrue village rumors, log world_events, and **unlock
  discoveries**. The `tunnels_open` beat sets `discovery_hidden_path`, unsealing
  the barrow road to Hollow Hill and the Mage-Ruins — new ground reachable *because
  the Dark opened it*. Wired into `DoomClock.pending_beats` (idempotent).
- **Flag-gated contracts** — notice-board postings can carry `requires_flag`, so
  the board responds to the spread: *Seal the Tunnel* (tunnels_open), *Tend the
  Forest Margin* (vines_breached), *Watch: The Walking Scarecrow* (scarecrow_awake)
  appear only once their world-sign falls.
- Tests in `tests/test_world_effects.py`; bundle at 44 concepts.

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
