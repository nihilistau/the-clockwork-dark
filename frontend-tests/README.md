# Frontend tests

Unit tests for the **pure** presentation helpers in
`content/scenes/clockwork/static/js/clockwork-helpers.js` — the side-effect-free
core that the browser bundle (`clockwork.js`) consumes via `window.ClockworkHelpers`.

```bash
cd frontend-tests
npm install      # one-time: pulls vitest
npm test         # vitest run
npm run test:watch
```

The harness covers `escapeHtml` (XSS escaping) and `challengeView` (deriving a
read-only challenge display from every spec shape). DOM-touching code stays in
`clockwork.js`; the a11y / escaping invariants are *also* guarded from the Python
suite by `tests/test_frontend_contract.py`, which runs with no Node toolchain.
