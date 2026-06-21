/*
 * Clockwork dialog focus manager
 * ==============================
 * a11y modal management, extracted from clockwork.js so it can be unit-tested
 * under jsdom. `create(doc)` wires a keydown handler on the document and returns
 * { openDialog, closeDialog, openCount }:
 *   - open dialogs are stacked; Escape closes the topmost;
 *   - Tab is trapped within the topmost dialog;
 *   - focus moves into a dialog on open and is restored to the opener on close.
 * No layout/offset checks (so it behaves identically in jsdom and the browser).
 */
(function (root, factory) {
  const api = factory();
  if (typeof module !== "undefined" && module.exports) {
    module.exports = api;
  }
  root.ClockworkDialogs = api;
})(typeof window !== "undefined" ? window : globalThis, function () {
  "use strict";

  const FOCUSABLE =
    'a[href], button:not([disabled]), textarea:not([disabled]), ' +
    'input:not([disabled]), select:not([disabled]), [tabindex]:not([tabindex="-1"])';

  function focusables(el) {
    return Array.from(el.querySelectorAll(FOCUSABLE));
  }

  function create(doc) {
    const stack = [];

    function openDialog(el) {
      if (!el) return;
      el.classList.remove("hidden");
      if (stack.some((e) => e.el === el)) return; // already open: don't re-stack / steal focus
      const opener = doc.activeElement;
      stack.push({ el, opener });
      const f = focusables(el);
      try { (f[0] || el).focus({ preventScroll: true }); } catch (e) {}
    }

    function closeDialog(el) {
      if (!el) return;
      el.classList.add("hidden");
      const idx = stack.map((e) => e.el).lastIndexOf(el);
      if (idx === -1) return;
      const entry = stack.splice(idx, 1)[0];
      const opener = entry && entry.opener;
      if (opener && typeof opener.focus === "function") {
        try { opener.focus({ preventScroll: true }); } catch (e) {}
      }
    }

    doc.addEventListener("keydown", (ev) => {
      if (!stack.length) return;
      const top = stack[stack.length - 1].el;
      if (ev.key === "Escape") {
        ev.preventDefault();
        closeDialog(top);
      } else if (ev.key === "Tab") {
        const f = focusables(top);
        if (!f.length) { ev.preventDefault(); try { top.focus(); } catch (e) {} return; }
        const first = f[0], last = f[f.length - 1];
        if (ev.shiftKey && doc.activeElement === first) { ev.preventDefault(); last.focus(); }
        else if (!ev.shiftKey && doc.activeElement === last) { ev.preventDefault(); first.focus(); }
      }
    });

    return { openDialog, closeDialog, openCount: () => stack.length };
  }

  return { create, focusables };
});
