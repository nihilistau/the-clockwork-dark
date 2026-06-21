const path = require("path");
const { defineConfig, devices } = require("@playwright/test");

// e2e smoke: Playwright starts the Flask game server itself (no LLM needed for
// the start screen / dialog behaviour) and waits on /api/health before testing.
module.exports = defineConfig({
  testDir: "./e2e",
  timeout: 30000,
  expect: { timeout: 5000 },
  fullyParallel: false,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 1 : 0,
  reporter: "list",
  use: {
    baseURL: "http://127.0.0.1:5573",
    trace: "on-first-retry",
  },
  projects: [{ name: "chromium", use: { ...devices["Desktop Chrome"] } }],
  webServer: {
    command: "python launcher.py clockwork --host 127.0.0.1 --port 5573",
    cwd: path.resolve(__dirname, ".."),
    url: "http://127.0.0.1:5573/api/health",
    reuseExistingServer: !process.env.CI,
    timeout: 60000,
  },
});
