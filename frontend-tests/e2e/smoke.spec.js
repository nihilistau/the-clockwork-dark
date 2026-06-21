const { test, expect } = require("@playwright/test");

test.describe("clockwork e2e smoke", () => {
  test("loads cleanly with the helper + dialog modules wired", async ({ page }) => {
    const errors = [];
    page.on("console", (m) => m.type() === "error" && errors.push(m.text()));
    page.on("pageerror", (e) => errors.push(String(e)));

    await page.goto("/");
    await expect(page).toHaveTitle(/CLOCKWORK DARK/i);
    await expect(page.locator("#start-screen")).toBeVisible();

    const wired = await page.evaluate(() => ({
      helpers: !!(window.ClockworkHelpers && window.ClockworkHelpers.escapeHtml),
      dialogs: !!(window.ClockworkDialogs && window.ClockworkDialogs.create),
      manager: !!(window.__clockworkDialogs && window.__clockworkDialogs.openDialog),
      micDisabled: document.getElementById("mic-btn").disabled === true,
      dialogCount: document.querySelectorAll('[role="dialog"]').length,
      tabindexCount: document.querySelectorAll('[role="dialog"][tabindex="-1"]').length,
    }));
    expect(wired.helpers).toBe(true);
    expect(wired.dialogs).toBe(true);
    expect(wired.manager).toBe(true);
    expect(wired.micDisabled).toBe(true);
    expect(wired.dialogCount).toBe(wired.tabindexCount);
    expect(wired.dialogCount).toBeGreaterThanOrEqual(4);

    // the only expected console error is a benign missing favicon
    const real = errors.filter((e) => !/favicon/i.test(e));
    expect(real, real.join("\n")).toHaveLength(0);
  });

  test("a dialog opens and Escape dismisses it via the real wired manager", async ({ page }) => {
    await page.goto("/");
    const panel = page.locator("#overlay-panel");
    await expect(panel).toBeHidden();

    // Drive the page's own dialog manager (the one whose keydown listener is live).
    await page.evaluate(() =>
      window.__clockworkDialogs.openDialog(document.getElementById("overlay-panel"))
    );
    await expect(panel).toBeVisible();

    await page.keyboard.press("Escape");
    await expect(panel).toBeHidden();
  });
});
