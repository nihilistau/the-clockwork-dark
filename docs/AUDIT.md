# Review & Audit — The Clockwork Dark

> **Latest: 2026-06-22 — full-codebase review/audit (v0.7).** Five-dimension review
> (correctness · security · architecture · tests · docs) over the whole engine,
> every finding verified against the code. Suite: **327 passing**. The prior
> 2026-06-21 audit (PR1–11 baseline) is retained below.

## 2026-06-22 — Full review & audit (v0.7)

**Verdict:** healthy and coherent. No critical defects — the
engine-resolves-mechanics boundary, secret hygiene, and config discipline all
hold. The findings were *tightenings*, not breakage; the high-value ones are
fixed in this pass.

### What's solid (verified, not assumed)
- **Secret hygiene** — `config/local.yaml` (holds the API key) is gitignored and
  was *never committed* (`git log -S` across all branches is clean); the key is
  never logged or returned in a payload; `/api/metrics` exposes only aggregates.
- **No dangerous primitives** — zero `eval`/`exec`/`pickle`/`os.system`; every YAML
  load is `safe_load`; the one `subprocess` call is an arg-list (no shell).
- **No path traversal** — `/design/<path>` uses `send_from_directory` (Werkzeug
  safe-join); no raw user-controlled file reads.
- **LLM is constrained** — tool dispatch rejects any name not in the `@skill`
  registry; outbound URLs come from config, never model text (no SSRF); Flask
  debug is off; challenge resolution is bounded (dice clamped, one step per call).
- **Save/load is complete** — `save_game` persists hidden + agent-mind state and
  round-trips through disk.

### Fixed in this pass (`feat/audit-tighten`)
| # | Severity | Finding | Fix |
|---|----------|---------|-----|
| 1 | Med · security | Server bound `0.0.0.0` + Socket.IO `cors="*"` by default — LAN exposure for a local-first app | Default `host: 127.0.0.1`; `security.cors_origins` localhost allow-list; `0.0.0.0` is now opt-in |
| 2 | Med · robustness | `/api/voice/transcribe` read uploads unbounded | `MAX_CONTENT_LENGTH` from `security.max_upload_mb` (8 MB) |
| 3 | Med · tech-debt | Assistant used a brittle non-greedy regex parser (the bug PR16 fixed for the Storyteller) — truncated on nested objects, broke on trailing commas | Assistant now shares `parsing.extract_json_object` + `normalize_tool_calls` |
| 4 | Med · frontend | `item.name` (model-controlled) rendered via raw `innerHTML` — XSS sink; rumor/foe text too | Routed through the existing `escapeHtml` |
| 5 | Low · correctness | `to_dict`/`from_dict` asymmetric — minds only persisted via `save_game`'s manual patch | Explicit `include_minds` flag; default payload stays client-safe |
| 6 | Low · security | AI-supplied challenge spec unbounded (state/save bloat) | Cap steps/nodes/outcomes; clamp puzzle attempts |
| 7 | Low · tech-debt | `_add_item` duplicated across four modules | One `engine/game/inventory.add_item`; thin provenance wrappers |
| 8 | Low · docs | README test badge/count stale (263) | → 318; status → PR1–37 |

All locked by `tests/test_audit_tighten.py` (9 tests); suite **327 passing**.

### Recommended next (not in this pass)
> **Update (follow-up PR):** the a11y, frontend-harness, and top backend-test-gap
> items below were **done** — and the new tests surfaced a real bug:
> `tool_dispatcher.execute_tool` was laundering a rejected required action (an
> illegal `move_to`) into a `success: True` receipt, so the Evaluator's
> failed-required-tool gate never fired; now fixed (dice resolvers excluded). Suite
> **359 passing** (+32). A jsdom/Playwright behavioural smoke is the remaining nice-to-have.

Higher-effort items surfaced by the review, for a follow-up:
- **Frontend a11y** — the four `role="dialog"` overlays have no Escape/focus-trap,
  and the doom-end modal can't be dismissed. Add keyboard handling + `:focus-visible`
  + a `prefers-reduced-motion` block.
- **Highest-value test gaps** — governance through the real route/socket (an R003
  violation reaching the payload); `chat_stream` HTTP-error/`ReadTimeout` → fallback;
  the "consumed" finale terminal; the contract double-complete guard; socket
  `narration_delta` + `error` paths; decision-tree branch/failure paths.
- **No automated frontend check** — add a jsdom unit test of the pure render helpers
  + a Playwright smoke (start → choice → overlay open/Escape).
- **Dead control** — the push-to-talk mic button has no handler; wire to STT or hide.

---

## 2026-06-21 — Prior audit (PR1–11 baseline)

_Date: 2026-06-21 · Scope: full codebase + design-asset integration · Baseline: PR1–PR11 complete._

## Summary

The project is in good health. The deterministic engine, dual-agent layer, media
pipeline, RAG lore, and Flask/Socket.IO scene are all implemented and tested. The
design system was bundled but not fully *driving* the UI; that gap is now closed
(see Phase C). No golden-rule violations remain after one fix.

| Area | Status |
|------|--------|
| Test suite | ✅ 123 passing (`pytest tests/ -q`, ~43s) |
| Config discipline (no hardcoded ports/models/paths) | ✅ after fix (see below) |
| Engine-resolves-mechanics boundary | ✅ enforced via `@skill` registry + Evaluator |
| Canon IDs (agents, locations, phases) | ✅ unchanged |
| Design-asset integration | ✅ now default + local-first |

## Tests

`pytest tests/ -q` → **123 passed**. 21 suites cover dice, evil ticker, locations,
skills enforcement, stream processing, storyteller/assistant agents, evaluator,
media, procgen, world-sim, lore/awareness, saves, the Flask scene, the design
manifest, and the PR12 vertical slice. The vertical-slice smoke test exercises all
nine PR12 acceptance criteria end-to-end with a mock LLM.

## Config discipline

All external endpoints and model names are resolved **config-first** with sensible
fallback defaults, e.g. `cfg.get("lmstudio.base_url", "http://localhost:1234/v1")`
(`engine/lmstudio/client.py`, `engine/media/{comfyui,tts,stt}.py`,
`engine/lmstudio/profiles.py`). These are correct, not violations.

**Fixed:** `engine/design/assets.py` previously hardcoded
`C:\Projects\clockwork-dark\Design_files` as a resolution fallback. Replaced with
repo-relative resolution (env `CLOCKWORK_DESIGN_FILES` → config `paths.design_files`
→ bundled `<repo>/Design_files`). `config/default.yaml` now defaults
`paths.design_files` to the repo-relative `"Design_files"` instead of a bare
`${CLOCKWORK_DESIGN_FILES}` env reference, so a fresh clone renders the full design
system with zero setup.

## Engine ↔ LLM boundary

The hard engine owns all mechanics; LLMs only narrate. Stat/inventory/travel/dice
changes flow exclusively through the `@skill` registry (`engine/skills/`), and the
Evaluator (`engine/agents/evaluator.py`) gates hallucinated mechanics with a retry.
`test_skill_enforcement.py` and `test_storyteller.py` cover this.

## Design-asset integration (resolved)

- **Media** (scene stills, intro, cutscenes, dice videos, portraits, items) was
  already mapped through `data/assets/manifest.yaml` + the `/design/<path>` Flask
  route. Verified: **113/113 referenced asset URLs exist on disk** (0 dangling).
- **Styling gap closed:** design tokens, the four type voices, and the phase-theme
  CSS now drive the live UI by default (previously behind a fragile conditional).
- **Local-first:** fonts were loading from the Google Fonts CDN; the four families
  are now vendored as `.woff2` under `Design_files/assets/fonts/` and served by the
  app, so play works fully offline.
- **Verified in-browser** (Playwright): `/design/styles.css` linked, fonts load
  locally, start screen + menu art + wordmark + 3 archetypes render, and the
  phase-theme creep advances `--surface-scene` (`#080b0b`→`#050706`) and
  `--corruption-reveal` (`0`→`1`) across dormant→consuming.

## Repository hygiene

Private repo `nihilistau/the-clockwork-dark`. `.gitignore` excludes the 8 redundant
ZIP source-bundles (incl. a 97 MB archive) and the `art-min/` duplicate; all runtime
art/video/tokens are committed (~340 MB) so a clone runs. `.gitattributes` normalizes
line endings and marks binaries. No committed file approaches GitHub's 100 MB limit.

## Operational note

Two leftover Flask servers from prior sessions were holding port 5573 and serving a
pre-start-screen template — a stale-process gotcha, not a code defect. `scripts/start.ps1`
should free the port before launch; consider adding a port-kill guard.

## Recommendations / next

1. **v0.2 features** (in progress): grounded combat (`resolve_combat`), crafting
   (`craft_item`), Millhaven march arc + cutscene milestones — each engine-authoritative
   and test-driven.
2. Optional: self-host the Socket.IO client (currently a CDN `<script>`) for full
   offline parity.
3. Optional: add a `start.ps1` port-free guard to avoid the stale-process gotcha.
