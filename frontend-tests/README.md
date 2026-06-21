# Frontend tests

Automated checks for the clockwork scene's client. Three layers:

| Layer | File(s) | Runner |
|-------|---------|--------|
| **Pure helpers** | `clockwork-helpers.test.js` | vitest (node) |
| **Dialog a11y behaviour** | `clockwork-dialogs.test.js` | vitest (**jsdom**) |
| **End-to-end smoke** | `e2e/smoke.spec.js` | Playwright (chromium) |

```bash
cd frontend-tests
npm install                       # one-time: vitest, jsdom, @playwright/test

npm test                          # unit + jsdom behaviour (vitest run)
npx playwright install chromium   # one-time: the browser binary
npm run test:e2e                  # Playwright boots the Flask server itself, then smokes it
```

- `clockwork-helpers.js` holds the **pure** presentation helpers (`escapeHtml`,
  `challengeView`); `clockwork-dialogs.js` holds the **a11y dialog manager**
  (open/Escape/focus-trap/restore). Both are consumed by `clockwork.js` via
  `window.*` and unit-tested here.
- The Playwright config starts `python launcher.py clockwork` and waits on
  `/api/health` — **no LLM needed** for the start screen + dialog smoke.
- The a11y/XSS invariants are *also* guarded from the Python suite by
  `tests/test_frontend_contract.py` (no Node toolchain required).

All three layers run in CI — see `.github/workflows/ci.yml`.
