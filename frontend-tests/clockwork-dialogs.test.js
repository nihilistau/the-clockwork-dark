/**
 * @vitest-environment jsdom
 *
 * Behavioural tests for the a11y dialog manager (clockwork-dialogs.js): open /
 * focus-in, Escape-to-close + focus-restore, stacking, and the Tab focus-trap.
 * Run as part of `npm test` (vitest).
 */
const {
  create,
  focusables,
} = require("../content/scenes/clockwork/static/js/clockwork-dialogs.js");

function mount() {
  document.body.innerHTML = `
    <button id="opener">Open</button>
    <div id="dlg" class="hidden" role="dialog" tabindex="-1">
      <button id="first">First</button>
      <button id="last">Last</button>
    </div>
    <div id="dlg2" class="hidden" role="dialog" tabindex="-1">
      <button id="b2">Two</button>
    </div>`;
  return create(document);
}

function press(key, shiftKey = false) {
  document.dispatchEvent(
    new KeyboardEvent("keydown", { key, shiftKey, bubbles: true, cancelable: true })
  );
}

const $ = (id) => document.getElementById(id);

describe("dialog focus manager", () => {
  beforeEach(() => {
    document.body.innerHTML = "";
  });

  it("opens: clears .hidden and moves focus to the first focusable", () => {
    const d = mount();
    $("opener").focus();
    d.openDialog($("dlg"));
    expect($("dlg").classList.contains("hidden")).toBe(false);
    expect(document.activeElement.id).toBe("first");
    expect(d.openCount()).toBe(1);
  });

  it("Escape closes the topmost dialog and restores focus to the opener", () => {
    const d = mount();
    $("opener").focus();
    d.openDialog($("dlg"));
    press("Escape");
    expect($("dlg").classList.contains("hidden")).toBe(true);
    expect(document.activeElement.id).toBe("opener");
    expect(d.openCount()).toBe(0);
  });

  it("stacks dialogs and closes them top-down on Escape", () => {
    const d = mount();
    d.openDialog($("dlg"));
    d.openDialog($("dlg2"));
    expect(d.openCount()).toBe(2);

    press("Escape");
    expect($("dlg2").classList.contains("hidden")).toBe(true);
    expect($("dlg").classList.contains("hidden")).toBe(false);

    press("Escape");
    expect($("dlg").classList.contains("hidden")).toBe(true);
    expect(d.openCount()).toBe(0);
  });

  it("traps Tab within the dialog (last→first, shift+first→last)", () => {
    const d = mount();
    d.openDialog($("dlg"));

    $("last").focus();
    press("Tab");
    expect(document.activeElement.id).toBe("first");

    $("first").focus();
    press("Tab", true);
    expect(document.activeElement.id).toBe("last");
  });

  it("opening an already-open dialog does not re-stack or steal focus", () => {
    const d = mount();
    d.openDialog($("dlg"));
    $("last").focus();
    d.openDialog($("dlg"));
    expect(d.openCount()).toBe(1);
    expect(document.activeElement.id).toBe("last");
  });

  it("ignores keys when no dialog is open", () => {
    const d = mount();
    $("opener").focus();
    press("Escape");
    expect(document.activeElement.id).toBe("opener");
    expect(d.openCount()).toBe(0);
  });

  it("focusables excludes disabled controls and tabindex=-1", () => {
    document.body.innerHTML =
      '<div id="d"><button>a</button><button disabled>b</button>' +
      '<div tabindex="-1">c</div><a href="#">l</a></div>';
    expect(focusables($("d")).length).toBe(2); // enabled button + anchor
  });
});
