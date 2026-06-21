/*
 * Clockwork pure helpers
 * ======================
 * Side-effect-free presentation helpers shared by the browser bundle
 * (clockwork.js, via window.ClockworkHelpers) and the vitest harness
 * (frontend-tests/, via require). No DOM access lives here — that's the point:
 * these are the unit-testable core.
 */
(function (root, factory) {
  const api = factory();
  if (typeof module !== "undefined" && module.exports) {
    module.exports = api;
  }
  root.ClockworkHelpers = api;
})(typeof window !== "undefined" ? window : globalThis, function () {
  "use strict";

  // Escape model-controlled text before it enters an innerHTML template.
  function escapeHtml(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  // Derive a read-only display from the active challenge dict (internal shape
  // from start_challenge, or the ChallengeResult.to_dict shape). Never throws
  // on a partial.
  function challengeView(ch) {
    ch = ch || {};
    const kind = String(ch.kind || "challenge");
    let text = ch.text || "";
    let options = Array.isArray(ch.options) ? ch.options.slice() : [];
    let answerRequired = !!ch.answer_required;
    const step = Number.isFinite(ch.step) ? ch.step : 0;
    const total =
      Number.isFinite(ch.total_steps) ? ch.total_steps :
      Array.isArray(ch.steps) ? ch.steps.length : 0;
    let meta = ch.message || "";
    let image = ch.image || "";        // optional scene art (set-pieces)
    let riddle = ch.riddle || "";      // optional parchment clue

    if (kind === "skill_gauntlet" && Array.isArray(ch.steps) && ch.steps.length) {
      const cur = ch.steps[Math.min(step, ch.steps.length - 1)] || {};
      if (!text) text = cur.text || "";
      if (!image) image = cur.image || "";
      if (!meta && (cur.skill || cur.dc != null)) {
        meta = `${cur.skill || "?"} · DC ${cur.dc != null ? cur.dc : "?"}`;
      }
      if (!options.length) options = [{ id: "attempt", text: "Attempt it" }];
    } else if (kind === "decision_tree" && ch.nodes && ch.current) {
      const node = ch.nodes[ch.current] || {};
      if (!text) text = node.text || "";
      if (!image) image = node.image || "";
      if (!riddle) riddle = node.riddle || node.clue || "";
      if (!options.length) {
        options = (node.options || []).map((o) => ({ id: o.id, text: o.text }));
      }
    } else if (kind === "puzzle") {
      answerRequired = true;
      if (!text) text = ch.prompt || ch.title || "";
      if (!meta && ch.attempts_left != null) meta = `${ch.attempts_left} attempts left`;
    } else if (kind === "dice_table") {
      if (!text) text = ch.prompt || ch.title || "";
      if (!options.length) options = [{ id: "roll", text: "Roll" }];
    }

    return { kind, text, options, answerRequired, step, total, meta, image, riddle };
  }

  return { escapeHtml, challengeView };
});
