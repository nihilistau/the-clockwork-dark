/* @ds-bundle: {"format":3,"namespace":"TheClockworkDarkDesignSystem_4a0a88","components":[{"name":"Badge","sourcePath":"components/core/Badge.jsx"},{"name":"Button","sourcePath":"components/core/Button.jsx"},{"name":"ChoiceChip","sourcePath":"components/core/ChoiceChip.jsx"},{"name":"StatLine","sourcePath":"components/core/StatLine.jsx"},{"name":"AssistantBubble","sourcePath":"components/feedback/AssistantBubble.jsx"},{"name":"DiceToast","sourcePath":"components/feedback/DiceToast.jsx"},{"name":"ScenePanel","sourcePath":"components/scene/ScenePanel.jsx"},{"name":"WorldClock","sourcePath":"components/scene/WorldClock.jsx"}],"sourceHashes":{"components/core/Badge.jsx":"7dadc1f78717","components/core/Button.jsx":"21c349de84a4","components/core/ChoiceChip.jsx":"403afd08e4b6","components/core/StatLine.jsx":"4fe379e1f83e","components/feedback/AssistantBubble.jsx":"09e4a9965577","components/feedback/DiceToast.jsx":"8b4a566f3e88","components/scene/ScenePanel.jsx":"c95f970f5cbe","components/scene/WorldClock.jsx":"bf1262b8965a","deck/deck-stage.js":"208980974db4","ui_kits/clockwork-scene/GameScene.jsx":"567c68b5c2b5","ui_kits/clockwork-world/App.jsx":"1c19d1ae63d1","ui_kits/clockwork-world/Atlas.jsx":"231fbbf55eb6","ui_kits/clockwork-world/Interface.jsx":"391d8ab8ec75","ui_kits/clockwork-world/PaintFrame.jsx":"26586e792755","ui_kits/clockwork-world/Screens.jsx":"235f9fcae1dc","ui_kits/clockwork-world/Souls.jsx":"cf27d89e3271","ui_kits/clockwork-world/Things.jsx":"40c6dbb899f6","ui_kits/clockwork-world/WorldKit.jsx":"cc98e214bff2","ui_kits/clockwork-world/data.js":"8fa83c0ebfe0"},"inlinedExternals":[],"unexposedExports":[]} */

(() => {

const __ds_ns = (window.TheClockworkDarkDesignSystem_4a0a88 = window.TheClockworkDarkDesignSystem_4a0a88 || {});

const __ds_scope = {};

(__ds_ns.__errors = __ds_ns.__errors || []);

// components/core/Badge.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Badge — a small tracked-smallcaps marker. Tones map to the
 * brand's restrained accent vocabulary. Used for the assistant
 * form tag, weather, phase, item tags.
 */
function Badge({
  tone = "neutral",
  style = {},
  children,
  ...rest
}) {
  const tones = {
    neutral: {
      bg: "transparent",
      fg: "var(--text-muted)",
      bd: "var(--iron-300)"
    },
    candle: {
      bg: "rgba(232,196,122,0.18)",
      fg: "var(--rust-700)",
      bd: "var(--tallow-700)"
    },
    brass: {
      bg: "transparent",
      fg: "var(--rust-clock)",
      bd: "var(--rust-clock)"
    },
    moss: {
      bg: "rgba(107,127,94,0.18)",
      fg: "var(--forest-700)",
      bd: "var(--moss-600)"
    },
    danger: {
      bg: "rgba(107,45,45,0.14)",
      fg: "var(--blood-quiet)",
      bd: "var(--blood-quiet)"
    },
    corruption: {
      bg: "rgba(122,158,79,0.16)",
      fg: "#52662f",
      bd: "var(--corruption)"
    }
  };
  const t = tones[tone] || tones.neutral;
  return /*#__PURE__*/React.createElement("span", _extends({
    style: {
      display: "inline-flex",
      alignItems: "center",
      gap: "0.3rem",
      fontFamily: "var(--font-ui)",
      fontSize: "var(--text-xs)",
      fontWeight: "var(--weight-semibold)",
      textTransform: "uppercase",
      letterSpacing: "var(--tracking-label)",
      color: t.fg,
      background: t.bg,
      border: `1px solid ${t.bd}`,
      borderRadius: "var(--radius-sm)",
      padding: "0.12rem 0.42rem",
      lineHeight: 1.5,
      ...style
    }
  }, rest), children);
}
Object.assign(__ds_scope, { Badge });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Badge.jsx", error: String((e && e.message) || e) }); }

// components/core/Button.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Button — the ledger-button. A pressed, candlelit control with
 * an iron edge. Hover deepens warmth; press insets. No scale tricks.
 */
function Button({
  variant = "primary",
  size = "md",
  disabled = false,
  type = "button",
  iconLeft = null,
  iconRight = null,
  style = {},
  children,
  ...rest
}) {
  const sizes = {
    sm: {
      padding: "0.35rem 0.7rem",
      font: "var(--text-sm)"
    },
    md: {
      padding: "0.5rem 0.95rem",
      font: "var(--text-base)"
    },
    lg: {
      padding: "0.65rem 1.25rem",
      font: "var(--text-md)"
    }
  };
  const variants = {
    primary: {
      background: "var(--accent-candle)",
      color: "var(--iron-900)",
      border: "var(--border-rule) solid var(--iron-700)"
    },
    secondary: {
      background: "var(--surface-card)",
      color: "var(--text-body)",
      border: "var(--border-rule) solid var(--iron-700)"
    },
    ghost: {
      background: "transparent",
      color: "var(--text-on-dark)",
      border: "var(--border-hair) solid var(--accent-candle)"
    },
    danger: {
      background: "var(--status-danger)",
      color: "var(--linen-100)",
      border: "var(--border-rule) solid var(--iron-900)"
    }
  };
  const s = sizes[size] || sizes.md;
  const v = variants[variant] || variants.primary;
  return /*#__PURE__*/React.createElement("button", _extends({
    type: type,
    disabled: disabled,
    "data-variant": variant,
    style: {
      display: "inline-flex",
      alignItems: "center",
      gap: "0.4rem",
      fontFamily: "var(--font-ui)",
      fontWeight: "var(--weight-semibold)",
      fontSize: s.font,
      lineHeight: 1,
      padding: s.padding,
      borderRadius: "var(--radius-sm)",
      cursor: disabled ? "wait" : "pointer",
      opacity: disabled ? 0.5 : 1,
      transition: "background var(--dur-fast) var(--ease-quiet), box-shadow var(--dur-fast) var(--ease-quiet), filter var(--dur-fast) var(--ease-quiet)",
      boxShadow: "var(--shadow-sm)",
      ...v,
      ...style
    },
    onMouseDown: e => {
      if (!disabled) e.currentTarget.style.boxShadow = "var(--shadow-inset)";
    },
    onMouseUp: e => {
      e.currentTarget.style.boxShadow = "var(--shadow-sm)";
    },
    onMouseEnter: e => {
      if (!disabled) e.currentTarget.style.filter = "brightness(0.93)";
    },
    onMouseLeave: e => {
      e.currentTarget.style.filter = "none";
      e.currentTarget.style.boxShadow = "var(--shadow-sm)";
    }
  }, rest), iconLeft, children, iconRight);
}
Object.assign(__ds_scope, { Button });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Button.jsx", error: String((e && e.message) || e) }); }

// components/core/ChoiceChip.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * ChoiceChip — a narrative choice pill (2–4 per turn). Keyboard
 * 1–4. Disables the instant it's clicked (the turn is in flight).
 * Shows an optional leading index key.
 */
function ChoiceChip({
  index = null,
  disabled = false,
  onClick,
  style = {},
  children,
  ...rest
}) {
  return /*#__PURE__*/React.createElement("button", _extends({
    type: "button",
    disabled: disabled,
    onClick: onClick,
    style: {
      display: "inline-flex",
      alignItems: "center",
      gap: "0.5rem",
      fontFamily: "var(--font-ui)",
      fontSize: "var(--text-base)",
      fontWeight: "var(--weight-medium)",
      color: "var(--iron-900)",
      background: "var(--accent-candle)",
      border: "var(--border-rule) solid var(--iron-700)",
      borderRadius: "var(--radius-sm)",
      padding: "0.5rem 0.85rem",
      cursor: disabled ? "wait" : "pointer",
      opacity: disabled ? 0.5 : 1,
      textAlign: "left",
      transition: "filter var(--dur-fast) var(--ease-quiet), box-shadow var(--dur-fast) var(--ease-quiet)",
      boxShadow: "var(--shadow-sm)",
      ...style
    },
    onMouseEnter: e => {
      if (!disabled) e.currentTarget.style.filter = "brightness(0.94)";
    },
    onMouseLeave: e => {
      e.currentTarget.style.filter = "none";
    }
  }, rest), index != null && /*#__PURE__*/React.createElement("span", {
    "aria-hidden": "true",
    style: {
      fontFamily: "var(--font-mono)",
      fontSize: "var(--text-xs)",
      color: "var(--rust-clock)",
      border: "1px solid var(--rust-clock)",
      borderRadius: "3px",
      padding: "0 0.3rem",
      lineHeight: 1.4
    }
  }, index), /*#__PURE__*/React.createElement("span", null, children));
}
Object.assign(__ds_scope, { ChoiceChip });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/ChoiceChip.jsx", error: String((e && e.message) || e) }); }

// components/core/StatLine.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * StatLine — a single ledger row: tracked label left, monospace
 * tabular value right, hairline rule between. The character sheet
 * is a stack of these.
 */
function StatLine({
  label,
  value,
  accent = false,
  style = {},
  ...rest
}) {
  return /*#__PURE__*/React.createElement("div", _extends({
    style: {
      display: "flex",
      justifyContent: "space-between",
      alignItems: "baseline",
      gap: "0.75rem",
      padding: "0.3rem 0",
      borderBottom: "var(--border-hair) solid var(--line-soft)",
      ...style
    }
  }, rest), /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: "var(--font-ui)",
      fontSize: "var(--text-xs)",
      textTransform: "uppercase",
      letterSpacing: "var(--tracking-label)",
      color: "var(--text-muted)"
    }
  }, label), /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: "var(--font-mono)",
      fontSize: "var(--text-sm)",
      fontWeight: "var(--weight-medium)",
      fontVariantNumeric: "tabular-nums",
      color: accent ? "var(--rust-clock)" : "var(--text-body)"
    }
  }, value));
}
Object.assign(__ds_scope, { StatLine });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/StatLine.jsx", error: String((e && e.message) || e) }); }

// components/feedback/AssistantBubble.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * AssistantBubble — the ambiguous helper's voice. Rounded sans,
 * linen card with a brass left edge and an open corner toward it.
 * Form tag in tracked smallcaps. `whisper` shrinks + italicizes
 * the text and lightens it. Max 3 lines by design — never a
 * tutorial fairy.
 */
function AssistantBubble({
  form = "cat",
  whisper = false,
  hidden = false,
  style = {},
  children,
  ...rest
}) {
  if (hidden) return null;
  return /*#__PURE__*/React.createElement("div", _extends({
    role: "status",
    style: {
      background: "var(--surface-card)",
      borderLeft: "var(--border-mark) solid var(--accent-brass)",
      borderRadius: "0 var(--radius-md) var(--radius-md) 0",
      padding: "0.7rem 0.85rem",
      boxShadow: "var(--shadow-card)",
      maxWidth: "100%",
      ...style
    }
  }, rest), /*#__PURE__*/React.createElement("span", {
    style: {
      display: "block",
      fontFamily: "var(--font-ui)",
      fontSize: "var(--text-xs)",
      textTransform: "uppercase",
      letterSpacing: "var(--tracking-label)",
      color: "var(--accent-brass)",
      marginBottom: "0.3rem"
    }
  }, form), /*#__PURE__*/React.createElement("p", {
    style: {
      margin: 0,
      fontFamily: "var(--font-assistant)",
      fontSize: whisper ? "var(--text-sm)" : "var(--text-base)",
      fontStyle: whisper ? "italic" : "normal",
      color: whisper ? "var(--text-muted)" : "var(--text-body)",
      lineHeight: "var(--leading-snug)",
      display: "-webkit-box",
      WebkitLineClamp: 3,
      WebkitBoxOrient: "vertical",
      overflow: "hidden"
    }
  }, children));
}
Object.assign(__ds_scope, { AssistantBubble });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/feedback/AssistantBubble.jsx", error: String((e && e.message) || e) }); }

// components/feedback/DiceToast.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * DiceToast — non-blocking center-screen result. Shows the engine's
 * dice line verbatim in mono, with the outcome word tinted by
 * result. Dwells ~1.5s then fades (caller handles timing/mount).
 */
function DiceToast({
  roll,
  modifier = 0,
  dc,
  outcome = "Success",
  style = {},
  ...rest
}) {
  const total = (Number(roll) || 0) + (Number(modifier) || 0);
  const sign = modifier >= 0 ? "+" : "−";
  const win = String(outcome).toLowerCase().startsWith("s");
  const outColor = win ? "var(--forest-500)" : "var(--blood-quiet)";
  return /*#__PURE__*/React.createElement("div", _extends({
    role: "status",
    style: {
      display: "inline-flex",
      alignItems: "center",
      gap: "0.6rem",
      fontFamily: "var(--font-mono)",
      fontSize: "var(--text-md)",
      background: "var(--surface-chrome)",
      color: "var(--text-on-dark)",
      border: "var(--border-rule) solid var(--accent-brass)",
      borderRadius: "var(--radius-sm)",
      padding: "0.7rem 1.1rem",
      boxShadow: "var(--shadow-raise)",
      ...style
    }
  }, rest), /*#__PURE__*/React.createElement("span", {
    style: {
      color: "var(--text-candlelight)"
    }
  }, "d20:"), /*#__PURE__*/React.createElement("span", {
    style: {
      fontVariantNumeric: "tabular-nums"
    }
  }, roll, " ", sign, " ", Math.abs(modifier), " = ", total), dc != null && /*#__PURE__*/React.createElement("span", {
    style: {
      color: "var(--text-muted)"
    }
  }, "vs DC ", dc), /*#__PURE__*/React.createElement("span", {
    style: {
      color: outColor,
      fontWeight: "var(--weight-semibold)"
    }
  }, "\u2014 ", outcome));
}
Object.assign(__ds_scope, { DiceToast });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/feedback/DiceToast.jsx", error: String((e && e.message) || e) }); }

// components/scene/ScenePanel.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * ScenePanel — a journal column surface (assistant / sheet). Tracked
 * smallcaps heading, optional iron edge on one side, paper-calm fill.
 * `surface` chooses the fill; `edge` places the 2px ledger rule.
 */
function ScenePanel({
  title = null,
  surface = "ledger",
  edge = "none",
  style = {},
  children,
  ...rest
}) {
  const surfaces = {
    ledger: "var(--surface-ledger)",
    panel: "var(--surface-panel)",
    narrative: "var(--surface-narrative)",
    card: "var(--surface-card)"
  };
  const edges = {
    none: {},
    left: {
      borderLeft: "var(--border-rule) solid var(--iron-700)"
    },
    right: {
      borderRight: "var(--border-rule) solid var(--iron-700)"
    }
  };
  return /*#__PURE__*/React.createElement("section", _extends({
    style: {
      background: surfaces[surface] || surfaces.ledger,
      padding: "var(--space-4)",
      minHeight: 0,
      ...edges[edge],
      ...style
    }
  }, rest), title && /*#__PURE__*/React.createElement("h2", {
    style: {
      margin: "0 0 var(--space-3)",
      fontFamily: "var(--font-ui)",
      fontSize: "var(--text-xs)",
      fontWeight: "var(--weight-semibold)",
      textTransform: "uppercase",
      letterSpacing: "var(--tracking-label)",
      color: "var(--text-body)"
    }
  }, title), children);
}
Object.assign(__ds_scope, { ScenePanel });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/scene/ScenePanel.jsx", error: String((e && e.message) || e) }); }

// components/scene/WorldClock.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * WorldClock — the chrome time readout. Monospace, candlelit, on
 * iron. Once the World Clock is *discovered* in-world, a small gear
 * glyph appears (set `discovered`). Until then it reads as plain
 * diegetic time. Format: "Day 12 · Evening".
 */
function WorldClock({
  day = 1,
  time = "Morning",
  discovered = false,
  style = {},
  ...rest
}) {
  return /*#__PURE__*/React.createElement("div", _extends({
    style: {
      display: "inline-flex",
      alignItems: "center",
      gap: "0.5rem",
      fontFamily: "var(--font-mono)",
      fontSize: "var(--text-sm)",
      color: "var(--text-candlelight)",
      letterSpacing: "0.02em",
      ...style
    }
  }, rest), discovered && /*#__PURE__*/React.createElement("span", {
    "aria-hidden": "true",
    style: {
      width: "13px",
      height: "13px",
      display: "inline-block",
      borderRadius: "50%",
      border: "1.5px solid var(--rust-300)",
      boxShadow: "inset 0 0 0 2px var(--surface-chrome)",
      position: "relative",
      top: "1px"
    }
  }), /*#__PURE__*/React.createElement("span", {
    style: {
      fontVariantNumeric: "tabular-nums"
    }
  }, "Day ", day, " \xB7 ", time));
}
Object.assign(__ds_scope, { WorldClock });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/scene/WorldClock.jsx", error: String((e && e.message) || e) }); }

// deck/deck-stage.js
try { (() => {
// @ds-adherence-ignore -- omelette starter scaffold (raw elements/hex/px by design)
/* ═══ THIS PROJECT USES DESIGN COMPONENTS (.dc.html) ═══
 * Reference this stage from your <x-dc> template as an import — NEVER as a
 * raw <deck-stage> tag plus a <script src> (that hides the whole deck until
 * the stream finishes):
 *
 *   <x-import component-from-global-scope="deck-stage" from="./deck-stage.js"
 *             width="1920" height="1080" hint-size="100%,100%">
 *     <section data-label="Title" style="...">…</section>
 *     <section data-label="Agenda" style="...">…</section>
 *   </x-import>
 *
 * Slides are inline-styled <section> siblings; do not add a stylesheet or a
 * deck-stage:not(:defined) rule. The plain-HTML "Usage" block in the comment
 * below does NOT apply to .dc.html templates.
 */
/* BEGIN USAGE */
/**
 * <deck-stage> — reusable web component for HTML decks.
 *
 * Handles:
 *  (a) speaker notes — reads <script type="application/json" id="speaker-notes">
 *      and posts {slideIndexChanged: N} to the parent window on nav.
 *  (b) keyboard navigation — ←/→, PgUp/PgDn, Space, Home/End, number keys.
 *      On touch devices, tapping the left/right half of the stage goes
 *      prev/next — taps on links, buttons and other interactive slide
 *      content are left alone.
 *  (c) press R to reset to slide 0 (with a tasteful keyboard hint).
 *  (d) bottom-center overlay showing slide count + hints, fades out on idle.
 *  (e) auto-scaling — inner canvas is a fixed design size (default 1920×1080)
 *      scaled with `transform: scale()` to fit the viewport, letterboxed.
 *      Set the `noscale` attribute to render at authored size (1:1) — the
 *      PPTX exporter sets this so its DOM capture sees unscaled geometry.
 *  (f) print — `@media print` lays every slide out as its own page at the
 *      design size, so the browser's Print → Save as PDF produces a clean
 *      one-page-per-slide PDF with no extra setup.
 *  (g) thumbnail rail — resizable left-hand column of per-slide thumbnails
 *      (static clones). Click to navigate; ↑/↓ with a thumbnail focused to
 *      step between slides; drag to reorder; right-click for
 *      Skip / Move up / Move down / Duplicate / Delete (Delete opens a
 *      Cancel/Delete confirm dialog). Drag the rail's right edge to resize;
 *      width persists to
 *      localStorage. Skipped slides carry `data-deck-skip`, are dimmed in
 *      the rail, omitted from prev/next navigation, and hidden at print.
 *      The rail is suppressed in presenting mode, in the host's Preview
 *      mode (ViewerMode='none'), on `noscale`, on narrow viewports
 *      (≤640px), and via the `no-rail` attribute. Rail mutations dispatch
 *      a `dc-op` CustomEvent on the element (see docs/dc-ops.md) and do
 *      NOT touch the DOM: the host applies the op and re-renders;
 *      structural rail input is locked until the host posts
 *      {__dc_op_ack: true, applied}.
 *
 * Slides are HIDDEN, not unmounted. Non-active slides stay in the DOM with
 * `visibility: hidden` + `opacity: 0`, so their state (videos, iframes,
 * form inputs, React trees) is preserved across navigation.
 *
 * Lifecycle event — the component dispatches a `slidechange` CustomEvent on
 * itself whenever the active slide changes (including the initial mount).
 * The event bubbles and composes out of shadow DOM, so you can listen on
 * the <deck-stage> element or on document:
 *
 *   document.querySelector('deck-stage').addEventListener('slidechange', (e) => {
 *     e.detail.index         // new 0-based index
 *     e.detail.previousIndex // previous index, or -1 on init
 *     e.detail.total         // total slide count
 *     e.detail.slide         // the new active slide element
 *     e.detail.previousSlide // the prior slide element, or null on init
 *     e.detail.reason        // 'init' | 'keyboard' | 'click' | 'tap' | 'api'
 *   });
 *
 * Persistence: none at the deck level. The host app keeps the current slide
 * in its own URL (?slide=) and re-delivers it via location.hash on load, so a
 * bare load with no hash always starts at slide 1.
 *
 * Usage:
 *   <style>deck-stage:not(:defined){visibility:hidden}</style>
 *   <deck-stage width="1920" height="1080">
 *     <section data-label="Title">...</section>
 *     <section data-label="Agenda">...</section>
 *   </deck-stage>
 *   <script src="deck-stage.js"></script>
 *
 * The :not(:defined) rule prevents a flash of the first slide at its
 * authored styles before this script runs and attaches the shadow root.
 *
 * Slides are the direct element children of <deck-stage>. Each slide is
 * automatically tagged with:
 *   - data-screen-label="NN Label"   (1-indexed, for comment flow)
 *   - data-om-validate="no_overflowing_text,no_overlapping_text,slide_sized_text"
 *
 * Speaker notes stay in sync because the component posts {slideIndexChanged: N}
 * to the parent — just include the #speaker-notes script tag if asked for notes.
 *
 * Authoring guidance:
 *   - Write slide bodies as static HTML inside <deck-stage>, with sizing via
 *     CSS custom properties in a <style> block rather than JS constants.
 *     Static slide markup is what lets the user click a heading in edit mode
 *     and retype it directly; a slide rendered through <script type="text/babel">,
 *     React, or a loop over a JS array has to round-trip every tweak through a
 *     chat message instead. Reach for script-generated slides only when the
 *     content genuinely needs interactive behaviour static HTML can't express.
 *   - Do NOT set position/inset/width/height on the slide <section> elements —
 *     the component absolutely positions every slotted child for you.
 *   - Entrance animations: make the visible end-state the base style and
 *     animate *from* hidden, so print and reduced-motion show content.
 *     Gate the animation on [data-deck-active] and the motion query, e.g.
 *     `@media (prefers-reduced-motion:no-preference){ [data-deck-active] .x{animation:fade-in .5s both} }`.
 *     Avoid infinite decorative loops on slide content.
 */
/* END USAGE */

(() => {
  const DESIGN_W_DEFAULT = 1920;
  const DESIGN_H_DEFAULT = 1080;
  const OVERLAY_HIDE_MS = 1800;
  const VALIDATE_ATTR = 'no_overflowing_text,no_overlapping_text,slide_sized_text';
  const FINE_POINTER_MQ = matchMedia('(hover: hover) and (pointer: fine)');
  const NARROW_MQ = matchMedia('(max-width: 640px)');
  // Slide-authored controls that should keep a tap instead of it navigating.
  const INTERACTIVE_SEL = 'a[href], button, input, select, textarea, summary, label, video[controls], audio[controls], [role="button"], [onclick], [tabindex]:not([tabindex^="-"]), [contenteditable]:not([contenteditable="false" i])';
  const pad2 = n => String(n).padStart(2, '0');

  // Label precedence: data-label → data-screen-label (number stripped) → first heading → "Slide".
  const getSlideLabel = el => {
    const explicit = el.getAttribute('data-label');
    if (explicit) return explicit;
    const existing = el.getAttribute('data-screen-label');
    if (existing) return existing.replace(/^\s*\d+\s*/, '').trim() || existing;
    const h = el.querySelector('h1, h2, h3, [data-title]');
    const t = h && (h.textContent || '').trim().slice(0, 40);
    if (t) return t;
    return 'Slide';
  };
  const stylesheet = `
    :host {
      position: fixed;
      inset: 0;
      display: block;
      background: #000;
      color: #fff;
      font-family: -apple-system, BlinkMacSystemFont, "Helvetica Neue", Helvetica, Arial, sans-serif;
      overflow: hidden;
      -webkit-tap-highlight-color: transparent;
    }
    /* connectedCallback holds this until document.fonts.ready (capped 2s) so
     * the first visible paint has the deck's real typography + final rail
     * layout. opacity (not visibility) so the active slide can't un-hide
     * itself via the ::slotted([data-deck-active]) visibility:visible rule.
     * Only the stage/rail hide — the black :host background stays, so the
     * iframe doesn't flash the page's default white. */
    :host([data-fonts-pending]) .stage,
    :host([data-fonts-pending]) .rail { opacity: 0; pointer-events: none; }

    .stage {
      position: absolute;
      inset: 0;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .canvas {
      position: relative;
      transform-origin: center center;
      flex-shrink: 0;
      background: #fff;
      will-change: transform;
    }

    /* Slides live in light DOM (via <slot>) so authored CSS still applies.
       We absolutely position each slotted child to stack them. */
    ::slotted(*) {
      position: absolute !important;
      inset: 0 !important;
      width: 100% !important;
      height: 100% !important;
      box-sizing: border-box !important;
      overflow: hidden;
      opacity: 0;
      pointer-events: none;
      visibility: hidden;
    }
    ::slotted([data-deck-active]) {
      opacity: 1;
      pointer-events: auto;
      visibility: visible;
    }

    .overlay {
      position: fixed;
      left: 50%;
      bottom: 22px;
      transform: translate(-50%, 6px) scale(0.92);
      filter: blur(6px);
      display: flex;
      align-items: center;
      gap: 4px;
      padding: 4px;
      background: #000;
      color: #fff;
      border-radius: 999px;
      font-size: 12px;
      font-feature-settings: "tnum" 1;
      letter-spacing: 0.01em;
      opacity: 0;
      pointer-events: none;
      transition: opacity 260ms ease, transform 260ms cubic-bezier(.2,.8,.2,1), filter 260ms ease;
      transform-origin: center bottom;
      z-index: 2147483000;
      user-select: none;
    }
    .overlay[data-visible] {
      opacity: 1;
      pointer-events: auto;
      transform: translate(-50%, 0) scale(1);
      filter: blur(0);
    }

    .btn {
      appearance: none;
      -webkit-appearance: none;
      background: transparent;
      border: 0;
      margin: 0;
      padding: 0;
      color: inherit;
      font: inherit;
      cursor: default;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      height: 28px;
      min-width: 28px;
      border-radius: 999px;
      color: rgba(255,255,255,0.72);
      transition: background 140ms ease, color 140ms ease;
      -webkit-tap-highlight-color: transparent;
    }
    .btn:hover { background: rgba(255,255,255,0.12); color: #fff; }
    .btn:active { background: rgba(255,255,255,0.18); }
    .btn:focus { outline: none; }
    .btn:focus-visible { outline: none; }
    .btn::-moz-focus-inner { border: 0; }
    .btn svg { width: 14px; height: 14px; display: block; }
    .btn.reset {
      font-size: 11px;
      font-weight: 500;
      letter-spacing: 0.02em;
      padding: 0 10px 0 12px;
      gap: 6px;
      color: rgba(255,255,255,0.72);
    }
    .btn.reset .kbd {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      min-width: 16px;
      height: 16px;
      padding: 0 4px;
      font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
      font-size: 10px;
      line-height: 1;
      color: rgba(255,255,255,0.88);
      background: rgba(255,255,255,0.12);
      border-radius: 4px;
    }

    .count {
      font-variant-numeric: tabular-nums;
      color: #fff;
      font-weight: 500;
      padding: 0 8px;
      min-width: 42px;
      text-align: center;
      font-size: 12px;
    }
    .count .sep { color: rgba(255,255,255,0.45); margin: 0 3px; font-weight: 400; }
    .count .total { color: rgba(255,255,255,0.55); }

    .divider {
      width: 1px;
      height: 14px;
      background: rgba(255,255,255,0.18);
      margin: 0 2px;
    }

    /* ── Thumbnail rail ──────────────────────────────────────────────────
       Fixed column on the left; each thumbnail is a static deep-clone of
       the light-DOM slide scaled into a 16:9 (or design-aspect) frame. The
       stage re-fits around it (see _fit); hidden during present / noscale
       / print so capture geometry and fullscreen output are unchanged. */
    .rail {
      position: fixed;
      left: 0;
      top: 0;
      bottom: 0;
      width: var(--deck-rail-w, 188px);
      background: #141414;
      border-right: 1px solid rgba(255,255,255,0.08);
      overflow-y: auto;
      overflow-x: hidden;
      padding: 12px 10px;
      box-sizing: border-box;
      display: flex;
      flex-direction: column;
      gap: 12px;
      z-index: 2147482500;
      scrollbar-width: thin;
      scrollbar-color: rgba(255,255,255,0.18) transparent;
    }
    .rail::-webkit-scrollbar { width: 8px; }
    .rail::-webkit-scrollbar-track { background: transparent; margin: 2px; }
    .rail::-webkit-scrollbar-thumb {
      background: rgba(255,255,255,0.18);
      border-radius: 4px;
      border: 2px solid transparent;
      background-clip: content-box;
    }
    .rail::-webkit-scrollbar-thumb:hover {
      background: rgba(255,255,255,0.28);
      border: 2px solid transparent;
      background-clip: content-box;
    }
    :host([no-rail]) .rail,
    :host([noscale]) .rail { display: none; }
    .rail[data-presenting] { display: none; }
    @media (max-width: 640px) {
      .rail, .rail-resize { display: none; }
    }
    /* User-driven show/hide (the TweaksPanel toggle) slides instead of
       popping. Transitions are gated on :host([data-rail-anim]) — set only
       for the 200ms around the toggle — so window-resize and rail-width
       drag (which also call _fit) don't lag behind the cursor. */
    .rail[data-user-hidden] { transform: translateX(-100%); }
    :host([data-rail-anim]) .rail { transition: transform 200ms cubic-bezier(.3,.7,.4,1); }
    :host([data-rail-anim]) .stage { transition: left 200ms cubic-bezier(.3,.7,.4,1); }
    :host([data-rail-anim]) .canvas { transition: transform 200ms cubic-bezier(.3,.7,.4,1); }
    /* transition shorthand replaces rather than merges — repeat the base
       .overlay opacity/transform/filter transitions so visibility changes
       during the 200ms toggle window still fade instead of popping. */
    :host([data-rail-anim]) .overlay {
      transition: margin-left 200ms cubic-bezier(.3,.7,.4,1),
                  opacity 260ms ease,
                  transform 260ms cubic-bezier(.2,.8,.2,1),
                  filter 260ms ease;
    }

    .thumb {
      position: relative;
      display: flex;
      align-items: flex-start;
      gap: 8px;
      cursor: pointer;
      user-select: none;
    }
    .thumb .num {
      width: 16px;
      flex-shrink: 0;
      font-size: 11px;
      font-weight: 500;
      text-align: right;
      color: rgba(255,255,255,0.55);
      padding-top: 2px;
      font-variant-numeric: tabular-nums;
    }
    .thumb .frame {
      position: relative;
      flex: 1;
      min-width: 0;
      aspect-ratio: var(--deck-aspect);
      background: #fff;
      border-radius: 4px;
      outline: 2px solid transparent;
      outline-offset: 0;
      overflow: hidden;
      transition: outline-color 120ms ease;
    }
    .thumb:hover .frame { outline-color: rgba(255,255,255,0.25); }
    .thumb { outline: none; }
    .thumb:focus-visible .frame { outline-color: rgba(255,255,255,0.5); }
    .thumb[data-current] .num { color: #fff; }
    .thumb[data-current] .frame { outline-color: #D97757; }
    .thumb[data-dragging] { opacity: 0.35; }
    .thumb::before {
      content: '';
      position: absolute;
      left: 24px;
      right: 0;
      height: 3px;
      border-radius: 2px;
      background: #D97757;
      opacity: 0;
      pointer-events: none;
    }
    .thumb[data-drop="before"]::before { top: -8px; opacity: 1; }
    .thumb[data-drop="after"]::before { bottom: -8px; opacity: 1; }
    .thumb[data-skip] .frame { opacity: 0.35; }
    .thumb[data-skip] .frame::after {
      content: 'Skipped';
      position: absolute;
      inset: 0;
      display: flex;
      align-items: center;
      justify-content: center;
      background: rgba(0,0,0,0.45);
      color: #fff;
      font-size: 10px;
      font-weight: 500;
      letter-spacing: 0.04em;
    }

    .ctxmenu {
      position: fixed;
      min-width: 150px;
      padding: 4px;
      background: #242424;
      border: 1px solid rgba(255,255,255,0.12);
      border-radius: 7px;
      box-shadow: 0 8px 24px rgba(0,0,0,0.45);
      z-index: 2147483100;
      display: none;
      font-size: 12px;
    }
    .ctxmenu[data-open] { display: block; }
    .ctxmenu button {
      display: block;
      width: 100%;
      appearance: none;
      border: 0;
      background: transparent;
      color: #e8e8e8;
      font: inherit;
      text-align: left;
      padding: 6px 10px;
      border-radius: 4px;
      cursor: pointer;
    }
    .ctxmenu button:hover:not(:disabled) { background: rgba(255,255,255,0.08); }
    .ctxmenu button:disabled { opacity: 0.35; cursor: default; }
    .ctxmenu hr {
      border: 0;
      border-top: 1px solid rgba(255,255,255,0.1);
      margin: 4px 2px;
    }

    .rail-resize {
      position: fixed;
      left: calc(var(--deck-rail-w, 188px) - 3px);
      top: 0;
      bottom: 0;
      width: 6px;
      cursor: col-resize;
      z-index: 2147482600;
      touch-action: none;
    }
    .rail-resize:hover,
    .rail-resize[data-dragging] { background: rgba(255,255,255,0.12); }
    :host([no-rail]) .rail-resize,
    :host([noscale]) .rail-resize,
    .rail[data-presenting] + .rail-resize,
    .rail[data-user-hidden] + .rail-resize { display: none; }

    /* Delete-confirm popup — matches the SPA's ConfirmDialog layout
       (title + message body, depressed footer with Cancel / Delete). */
    .confirm-backdrop {
      position: fixed;
      inset: 0;
      background: rgba(0,0,0,0.45);
      z-index: 2147483200;
      display: none;
      align-items: center;
      justify-content: center;
    }
    .confirm-backdrop[data-open] { display: flex; }
    .confirm {
      width: 320px;
      max-width: calc(100vw - 32px);
      background: #2a2a2a;
      color: #e8e8e8;
      border: 1px solid rgba(255,255,255,0.12);
      border-radius: 12px;
      box-shadow: 0 12px 32px rgba(0,0,0,0.5);
      overflow: hidden;
      font-family: inherit;
      animation: deck-confirm-in 0.18s ease;
    }
    @keyframes deck-confirm-in {
      from { opacity: 0; transform: scale(0.96); }
      to { opacity: 1; transform: scale(1); }
    }
    .confirm .body { padding: 20px 20px 16px; }
    .confirm .title { font-size: 14px; font-weight: 600; margin-bottom: 4px; }
    .confirm .msg { font-size: 13px; line-height: 1.5; color: rgba(255,255,255,0.65); }
    .confirm .footer {
      padding: 14px 20px;
      background: #1f1f1f;
      border-top: 1px solid rgba(255,255,255,0.08);
      display: flex;
      justify-content: flex-end;
      gap: 8px;
    }
    .confirm button {
      appearance: none;
      font: inherit;
      font-size: 13px;
      font-weight: 500;
      padding: 8px 16px;
      border-radius: 8px;
      cursor: pointer;
    }
    .confirm .cancel {
      background: transparent;
      border: 0;
      color: rgba(255,255,255,0.8);
    }
    .confirm .cancel:hover { background: rgba(255,255,255,0.08); }
    .confirm .danger {
      background: #c96442;
      border: 1px solid rgba(0,0,0,0.15);
      color: #fff;
      box-shadow: 0 1px 3px rgba(166,50,68,0.3), 0 2px 6px rgba(166,50,68,0.18);
    }
    .confirm .danger:hover { background: #b5563a; }

    /* ── Print: one page per slide, no chrome ────────────────────────────
       The screen layout stacks every slide at inset:0 inside a scaled
       canvas; for print we want them in document flow at the authored
       design size so the browser paginates one slide per sheet. The
       @page size is set from the width/height attributes via the inline
       <style id="deck-stage-print-page"> that _syncPrintPageRule appends
       to the document (the @page at-rule has no effect inside shadow DOM). */
    @media print {
      :host {
        position: static;
        inset: auto;
        background: none;
        overflow: visible;
        color: inherit;
      }
      .stage { position: static; display: block; }
      .canvas {
        transform: none !important;
        width: auto !important;
        height: auto !important;
        background: none;
        will-change: auto;
      }
      ::slotted(*) {
        position: relative !important;
        inset: auto !important;
        width: var(--deck-design-w) !important;
        height: var(--deck-design-h) !important;
        box-sizing: border-box !important;
        opacity: 1 !important;
        visibility: visible !important;
        pointer-events: auto;
        break-after: page;
        page-break-after: always;
        break-inside: avoid;
        overflow: hidden;
      }
      /* :last-child alone isn't enough once data-deck-skip hides the
         trailing slide(s) — the last *visible* slide still carries
         break-after:page and prints a blank sheet. _markLastVisible()
         maintains data-deck-last-visible on the last non-skipped slide. */
      ::slotted(*:last-child),
      ::slotted([data-deck-last-visible]) {
        break-after: auto;
        page-break-after: auto;
      }
      ::slotted([data-deck-skip]) { display: none !important; }
      .overlay, .rail, .rail-resize, .ctxmenu, .confirm-backdrop { display: none !important; }
    }
  `;
  class DeckStage extends HTMLElement {
    static get observedAttributes() {
      return ['width', 'height', 'noscale', 'no-rail'];
    }
    constructor() {
      super();
      this._root = this.attachShadow({
        mode: 'open'
      });
      this._index = 0;
      this._slides = [];
      this._notes = [];
      this._hideTimer = null;
      this._mouseIdleTimer = null;
      this._menuIndex = -1;
      this._onKey = this._onKey.bind(this);
      this._onResize = this._onResize.bind(this);
      this._onSlotChange = this._onSlotChange.bind(this);
      this._onMouseMove = this._onMouseMove.bind(this);
      this._onTap = this._onTap.bind(this);
      this._onMessage = this._onMessage.bind(this);
      // Capture-phase close so a click anywhere dismisses the menu, but
      // ignore clicks that land inside the menu itself — otherwise the
      // capture handler runs before the menu's own (bubble) handler and
      // clears _menuIndex out from under it.
      this._onDocClick = e => {
        if (this._menu && e.composedPath && e.composedPath().includes(this._menu)) return;
        this._closeMenu();
      };
    }
    get designWidth() {
      return parseInt(this.getAttribute('width'), 10) || DESIGN_W_DEFAULT;
    }
    get designHeight() {
      return parseInt(this.getAttribute('height'), 10) || DESIGN_H_DEFAULT;
    }
    connectedCallback() {
      // Presenter-view popup loads deckUrl?_snthumb=...#N for its prev/cur/
      // next thumbnails — the rail has no business rendering inside those
      // (wrong scale, and it offsets the stage so the thumb shows a gutter).
      if (/[?&]_snthumb=/.test(location.search)) this.setAttribute('no-rail', '');
      this._render();
      this._loadNotes();
      this._syncPrintPageRule();
      window.addEventListener('keydown', this._onKey);
      window.addEventListener('resize', this._onResize);
      window.addEventListener('mousemove', this._onMouseMove, {
        passive: true
      });
      window.addEventListener('message', this._onMessage);
      window.addEventListener('click', this._onDocClick, true);
      this.addEventListener('click', this._onTap);
      // Print lays every slide out as its own page, so [data-deck-active]-
      // gated entrance styles need the attribute on every slide (not just
      // the current one) or their content prints at the hidden base style.
      // The transient freeze style lands BEFORE the attributes so any
      // attribute-keyed transition fires at 0s (changing transition-
      // duration after a transition has started doesn't affect it).
      this._onBeforePrint = () => {
        this._syncPrintPageRule();
        if (this._freezeStyle) this._freezeStyle.remove();
        this._freezeStyle = document.createElement('style');
        this._freezeStyle.textContent = '*,*::before,*::after{transition-duration:0s !important}';
        document.head.appendChild(this._freezeStyle);
        this._slides.forEach(s => s.setAttribute('data-deck-active', ''));
      };
      this._onAfterPrint = () => {
        this._applyIndex({
          showOverlay: false,
          broadcast: false
        });
        if (this._freezeStyle) {
          this._freezeStyle.remove();
          this._freezeStyle = null;
        }
      };
      window.addEventListener('beforeprint', this._onBeforePrint);
      window.addEventListener('afterprint', this._onAfterPrint);
      // Initial collection + layout happens via slotchange, which fires on mount.
      this._enableRail();
      // Hold the stage hidden until webfonts are ready so the first visible
      // paint has the deck's real typography — the :not(:defined) guard in
      // the page HTML only covers custom-element upgrade, not font load.
      // Capped so a 404'd font URL can't blank the deck indefinitely.
      this.setAttribute('data-fonts-pending', '');
      const reveal = () => this.removeAttribute('data-fonts-pending');
      // rAF first: fonts.ready is a pre-resolved promise until layout has
      // resolved the slotted text's font-family and pushed a FontFace into
      // 'loading'. Reading it here in connectedCallback (parse-time) would
      // settle the race in a microtask before any font fetch starts.
      requestAnimationFrame(() => {
        Promise.race([document.fonts ? document.fonts.ready : Promise.resolve(), new Promise(r => setTimeout(r, 2000))]).then(reveal, reveal);
      });
    }
    _enableRail() {
      // Idempotent — older host builds still post __omelette_rail_enabled.
      // no-rail guard keeps the observers/stylesheet walk off the cheap path
      // for presenter-popup thumbnail iframes (up to 9 per view).
      if (this._railEnabled || this.hasAttribute('no-rail')) return;
      this._railEnabled = true;
      // Per-viewer preference — restored alongside rail width. Default on;
      // only a stored '0' (from the TweaksPanel toggle) hides it.
      this._railVisible = true;
      try {
        if (localStorage.getItem('deck-stage.railVisible') === '0') this._railVisible = false;
      } catch (e) {}
      // Live thumbnail updates: watch the light-DOM slides for content
      // edits and re-clone just the affected thumb(s), debounced. Ignore
      // the data-deck-* / data-screen-label / data-om-validate attributes
      // this component itself writes so nav doesn't trigger spurious
      // refreshes — except data-deck-skip, which now arrives from the host
      // re-render and is what updates the rail badge, print bookkeeping,
      // and deckSkipped re-broadcast.
      const OWN_ATTRS = /^data-(deck-(?!skip$)|screen-label$|om-validate$)/;
      this._liveDirty = new Set();
      this._liveObserver = new MutationObserver(records => {
        for (const r of records) {
          if (r.type === 'attributes' && OWN_ATTRS.test(r.attributeName || '')) continue;
          let n = r.target;
          while (n && n.parentElement !== this) n = n.parentElement;
          // Skip/unskip is handled below without re-cloning (the badge sits
          // on the thumb wrapper, not the clone) — don't mark the slide
          // dirty for an attr change whose only visible effect is the badge.
          if (n && this._slideSet && this._slideSet.has(n) && !(r.type === 'attributes' && r.attributeName === 'data-deck-skip')) {
            this._liveDirty.add(n);
          }
          // Host-driven skip toggle: sync the rail badge + print + presenter
          // skipped-list the way _toggleSkip used to do locally.
          if (r.type === 'attributes' && r.attributeName === 'data-deck-skip' && n && this._slideSet && this._slideSet.has(n)) {
            const i = this._slides.indexOf(n);
            if (this._thumbs && this._thumbs[i]) {
              if (n.hasAttribute('data-deck-skip')) this._thumbs[i].thumb.setAttribute('data-skip', '');else this._thumbs[i].thumb.removeAttribute('data-skip');
            }
            this._markLastVisible();
            try {
              window.postMessage({
                slideIndexChanged: this._index,
                deckTotal: this._slides.length,
                deckSkipped: this._skippedIndices()
              }, '*');
            } catch (e) {}
          }
        }
        if (this._liveDirty.size && !this._liveTimer) {
          this._liveTimer = setTimeout(() => {
            this._liveTimer = null;
            this._liveDirty.forEach(s => this._refreshThumb(s));
            this._liveDirty.clear();
          }, 200);
        }
      });
      this._liveObserver.observe(this, {
        subtree: true,
        childList: true,
        characterData: true,
        attributes: true
      });
      // Lazy thumbnail materialization — clone the slide only when its
      // frame scrolls into (or near) the rail viewport. rootMargin gives
      // ~4 thumbs of pre-load so fast scrolling doesn't flash blanks.
      this._railObserver = new IntersectionObserver(entries => {
        entries.forEach(e => {
          if (e.isIntersecting && e.target.__deckThumb) {
            this._materialize(e.target.__deckThumb);
          }
        });
      }, {
        root: this._rail,
        rootMargin: '400px 0px'
      });
      // Tweaks typically change CSS vars / attrs OUTSIDE <deck-stage>
      // (on <html>, <body>, a wrapper div, or a <style> tag), which
      // _liveObserver can't see. Re-snapshot author CSS (constructable
      // sheet is shared by reference, so one replaceSync updates every
      // thumb shadow root) and re-sync each thumb host's attrs + custom
      // properties. In-slide DOM mutations are _liveObserver's job.
      // Debounced so slider drags don't thrash.
      this._onTweakChange = () => {
        clearTimeout(this._tweakTimer);
        this._tweakTimer = setTimeout(() => {
          this._snapshotAuthorCss();
          // One getComputedStyle for the whole batch — each
          // getPropertyValue read below reuses the same computed style
          // as long as nothing invalidates layout between thumbs.
          const cs = getComputedStyle(this);
          (this._thumbs || []).forEach(t => {
            if (t.host) this._syncThumbHostAttrs(t.host, cs);
          });
        }, 120);
      };
      window.addEventListener('tweakchange', this._onTweakChange);
      this._snapshotAuthorCss();
      // Build the rail now that it's enabled — slotchange already fired,
      // so _renderRail's early-return skipped the initial build.
      this._syncRailHidden();
      this._renderRail();
      this._fit();
    }

    /** Snapshot document stylesheets into a constructable sheet that each
     *  thumbnail's nested shadow root adopts — so author CSS styles the
     *  cloned slide content without touching this component's chrome.
     *  Cross-origin sheets throw on .cssRules — skip them. Re-callable:
     *  the existing constructable sheet is reused via replaceSync so every
     *  already-adopted shadow root picks up the fresh CSS without re-adopt. */
    _snapshotAuthorCss() {
      // :root in an adopted sheet inside a shadow root matches nothing
      // (only the document root qualifies), so author rules like
      // `:root[data-voice="modern"] .serif` never reach the clones.
      // Rewrite :root → :host and mirror <html>'s data-*/class/lang onto
      // each thumb host (see _syncThumbHostAttrs) so the same selectors
      // match inside the thumbnail's shadow tree.
      const authorCss = Array.from(document.styleSheets).map(sh => {
        try {
          return Array.from(sh.cssRules).map(r => r.cssText).join('\n');
        } catch (e) {
          return '';
        }
      }).join('\n')
      // The shadow host is featureless outside the functional :host(...)
      // form, so any compound on :root — [attr], .class, #id, :pseudo —
      // must become :host(<compound>) not :host<compound>. Same for the
      // html type selector (Tailwind class-strategy dark mode emits
      // html.dark; Pico uses html[data-theme]), which has nothing to
      // match inside the thumb's shadow tree.
      .replace(/:root((?:\[[^\]]*\]|[.#][-\w]+|:[-\w]+(?:\([^)]*\))?)+)/g, ':host($1)').replace(/:root\b/g, ':host').replace(/(^|[\s,>~+(}])html((?:\[[^\]]*\]|[.#][-\w]+|:[-\w]+(?:\([^)]*\))?)+)(?![-\w])/g, '$1:host($2)').replace(/(^|[\s,>~+(}])html(?![-\w])/g, '$1:host');
      // Every custom property the author references. _syncThumbHostAttrs
      // mirrors each one's *computed* value at <deck-stage> onto the
      // thumb host so the live value wins over the :host default above
      // regardless of which ancestor the tweak wrote to (<html>, <body>,
      // a wrapper div, or the deck-stage element itself all inherit
      // down to getComputedStyle(this)).
      this._authorVars = new Set(authorCss.match(/--[\w-]+/g) || []);
      try {
        if (!this._adoptedSheet) this._adoptedSheet = new CSSStyleSheet();
        this._adoptedSheet.replaceSync(authorCss);
      } catch (e) {
        this._adoptedSheet = null;
        this._authorCss = authorCss;
      }
    }
    _syncThumbHostAttrs(host, cs) {
      const de = document.documentElement;
      // setAttribute overwrites but can't delete — an attr removed from
      // <html> (toggleAttribute off, classList emptied) would linger on
      // the host and :host([data-*]) / :host(.foo) rules would keep
      // matching. Remove stale mirrored attrs first; iterate backward
      // because removeAttribute mutates the live NamedNodeMap.
      for (let i = host.attributes.length - 1; i >= 0; i--) {
        const n = host.attributes[i].name;
        if ((n.startsWith('data-') || n === 'class' || n === 'lang') && !de.hasAttribute(n)) {
          host.removeAttribute(n);
        }
      }
      for (const a of de.attributes) {
        if (a.name.startsWith('data-') || a.name === 'class' || a.name === 'lang') {
          host.setAttribute(a.name, a.value);
        }
      }
      // The :root→:host rewrite in _snapshotAuthorCss pins each custom
      // property to its stylesheet default on the thumb host, shadowing
      // the live value that would otherwise inherit. Tweaks can write the
      // live value on any ancestor — <html>, <body>, a wrapper div, the
      // deck-stage element — so read it as the *computed* value at
      // <deck-stage> (which sees the whole inheritance chain) rather than
      // trying to guess which element the author wrote to. Inline on the
      // host beats the :host{} rule. remove-stale covers vars dropped
      // from the stylesheet between snapshots.
      const vars = this._authorVars || new Set();
      for (let i = host.style.length - 1; i >= 0; i--) {
        const p = host.style[i];
        if (p.startsWith('--') && !vars.has(p)) host.style.removeProperty(p);
      }
      const live = cs || getComputedStyle(this);
      vars.forEach(p => {
        const v = live.getPropertyValue(p);
        if (v) host.style.setProperty(p, v.trim());else host.style.removeProperty(p);
      });
    }
    disconnectedCallback() {
      window.removeEventListener('keydown', this._onKey);
      window.removeEventListener('resize', this._onResize);
      window.removeEventListener('mousemove', this._onMouseMove);
      window.removeEventListener('message', this._onMessage);
      window.removeEventListener('click', this._onDocClick, true);
      window.removeEventListener('beforeprint', this._onBeforePrint);
      window.removeEventListener('afterprint', this._onAfterPrint);
      if (this._freezeStyle) {
        this._freezeStyle.remove();
        this._freezeStyle = null;
      }
      this.removeEventListener('click', this._onTap);
      if (this._hideTimer) clearTimeout(this._hideTimer);
      if (this._mouseIdleTimer) clearTimeout(this._mouseIdleTimer);
      if (this._liveTimer) clearTimeout(this._liveTimer);
      if (this._tweakTimer) clearTimeout(this._tweakTimer);
      if (this._railAnimTimer) clearTimeout(this._railAnimTimer);
      if (this._scaleRaf) cancelAnimationFrame(this._scaleRaf);
      if (this._liveObserver) this._liveObserver.disconnect();
      if (this._railObserver) this._railObserver.disconnect();
      if (this._onTweakChange) window.removeEventListener('tweakchange', this._onTweakChange);
    }
    attributeChangedCallback() {
      if (this._canvas) {
        this._canvas.style.width = this.designWidth + 'px';
        this._canvas.style.height = this.designHeight + 'px';
        this._canvas.style.setProperty('--deck-design-w', this.designWidth + 'px');
        this._canvas.style.setProperty('--deck-design-h', this.designHeight + 'px');
        if (this._rail) {
          this._rail.style.setProperty('--deck-aspect', this.designWidth + '/' + this.designHeight);
        }
        this._fit();
        this._scaleThumbs();
        this._syncPrintPageRule();
      }
    }
    _render() {
      const style = document.createElement('style');
      style.textContent = stylesheet;
      const stage = document.createElement('div');
      stage.className = 'stage';
      const canvas = document.createElement('div');
      canvas.className = 'canvas';
      canvas.style.width = this.designWidth + 'px';
      canvas.style.height = this.designHeight + 'px';
      canvas.style.setProperty('--deck-design-w', this.designWidth + 'px');
      canvas.style.setProperty('--deck-design-h', this.designHeight + 'px');
      const slot = document.createElement('slot');
      slot.addEventListener('slotchange', this._onSlotChange);
      canvas.appendChild(slot);
      stage.appendChild(canvas);

      // Overlay: compact, solid black, with clickable controls.
      const overlay = document.createElement('div');
      overlay.className = 'overlay export-hidden';
      overlay.setAttribute('role', 'toolbar');
      overlay.setAttribute('aria-label', 'Deck controls');
      overlay.setAttribute('data-omelette-chrome', '');
      overlay.innerHTML = `
        <button class="btn prev" type="button" aria-label="Previous slide" title="Previous (←)">
          <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M10 3L5 8l5 5"/></svg>
        </button>
        <span class="count" aria-live="polite"><span class="current">1</span><span class="sep">/</span><span class="total">1</span></span>
        <button class="btn next" type="button" aria-label="Next slide" title="Next (→)">
          <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 3l5 5-5 5"/></svg>
        </button>
        <span class="divider"></span>
        <button class="btn reset" type="button" aria-label="Reset to first slide" title="Reset (R)">Reset<span class="kbd">R</span></button>
      `;
      overlay.querySelector('.prev').addEventListener('click', () => this._advance(-1, 'click'));
      overlay.querySelector('.next').addEventListener('click', () => this._advance(1, 'click'));
      overlay.querySelector('.reset').addEventListener('click', () => this._go(0, 'click'));

      // Thumbnail rail + context menu. Thumbnails are populated in
      // _renderRail() after _collectSlides().
      const rail = document.createElement('div');
      rail.className = 'rail export-hidden';
      rail.setAttribute('data-omelette-chrome', '');
      // Edit mode hooks wheel to pan the canvas; this opts the rail's own
      // scrollview out so thumbnails stay scrollable while editing.
      rail.setAttribute('data-dc-wheel-passthru', '');
      rail.style.setProperty('--deck-aspect', this.designWidth + '/' + this.designHeight);
      // Edge auto-scroll while dragging a thumb near the rail's top/bottom
      // so off-screen drop targets are reachable. Native dragover fires
      // continuously while the pointer is stationary, so a per-event nudge
      // (ramped by edge proximity) is enough — no rAF loop needed.
      rail.addEventListener('dragover', e => {
        if (this._dragFrom == null) return;
        const r = rail.getBoundingClientRect();
        const EDGE = 40;
        const dt = e.clientY - r.top;
        const db = r.bottom - e.clientY;
        if (dt < EDGE) rail.scrollTop -= Math.ceil((EDGE - dt) / 3);else if (db < EDGE) rail.scrollTop += Math.ceil((EDGE - db) / 3);
      });
      const menu = document.createElement('div');
      menu.className = 'ctxmenu export-hidden';
      menu.setAttribute('data-omelette-chrome', '');
      menu.innerHTML = `
        <button type="button" data-act="skip">Skip slide</button>
        <button type="button" data-act="up">Move up</button>
        <button type="button" data-act="down">Move down</button>
        <button type="button" data-act="duplicate">Duplicate slide</button>
        <hr>
        <button type="button" data-act="delete">Delete slide</button>
      `;
      menu.addEventListener('click', e => {
        const act = e.target && e.target.getAttribute && e.target.getAttribute('data-act');
        if (!act) return;
        const i = this._menuIndex;
        this._closeMenu();
        if (act === 'skip') this._toggleSkip(i);else if (act === 'up') this._moveSlide(i, i - 1);else if (act === 'down') this._moveSlide(i, i + 1);else if (act === 'duplicate') this._duplicateSlide(i);else if (act === 'delete') this._openConfirm(i);
      });
      menu.addEventListener('contextmenu', e => e.preventDefault());

      // Rail resize handle — drag to set --deck-rail-w, persisted to
      // localStorage so the width survives reloads.
      const resize = document.createElement('div');
      resize.className = 'rail-resize export-hidden';
      resize.setAttribute('data-omelette-chrome', '');
      resize.addEventListener('pointerdown', e => {
        e.preventDefault();
        resize.setPointerCapture(e.pointerId);
        resize.setAttribute('data-dragging', '');
        const move = ev => this._setRailWidth(ev.clientX);
        const up = () => {
          resize.removeEventListener('pointermove', move);
          resize.removeEventListener('pointerup', up);
          resize.removeEventListener('pointercancel', up);
          resize.removeAttribute('data-dragging');
          try {
            localStorage.setItem('deck-stage.railWidth', String(this._railPx));
          } catch (err) {}
        };
        resize.addEventListener('pointermove', move);
        resize.addEventListener('pointerup', up);
        resize.addEventListener('pointercancel', up);
      });

      // Delete-confirm dialog — mirrors the SPA's ConfirmDialog layout.
      const confirm = document.createElement('div');
      confirm.className = 'confirm-backdrop export-hidden';
      confirm.setAttribute('data-omelette-chrome', '');
      confirm.innerHTML = `
        <div class="confirm" role="dialog" aria-modal="true">
          <div class="body">
            <div class="title">Delete slide?</div>
            <div class="msg">This slide will be removed from the deck.</div>
          </div>
          <div class="footer">
            <button type="button" class="cancel">Cancel</button>
            <button type="button" class="danger">Delete</button>
          </div>
        </div>
      `;
      confirm.addEventListener('click', e => {
        if (e.target === confirm) this._closeConfirm();
      });
      confirm.querySelector('.cancel').addEventListener('click', () => this._closeConfirm());
      confirm.querySelector('.danger').addEventListener('click', () => {
        const i = this._confirmIndex;
        this._closeConfirm();
        this._deleteSlide(i);
      });
      this._root.append(style, rail, resize, stage, overlay, menu, confirm);
      this._canvas = canvas;
      this._stage = stage;
      this._slot = slot;
      this._overlay = overlay;
      this._rail = rail;
      this._resize = resize;
      this._menu = menu;
      this._confirm = confirm;
      this._countEl = overlay.querySelector('.current');
      this._totalEl = overlay.querySelector('.total');

      // Restore persisted rail width.
      let rw = 188;
      try {
        const s = localStorage.getItem('deck-stage.railWidth');
        if (s) rw = parseInt(s, 10) || rw;
      } catch (err) {}
      this._setRailWidth(rw);
      this._syncRailHidden();
    }
    _setRailWidth(px) {
      const w = Math.max(120, Math.min(360, Math.round(px)));
      this._railPx = w;
      this.style.setProperty('--deck-rail-w', w + 'px');
      this._fit();
      // _scaleThumbs forces a sync layout (frame.offsetWidth) then writes
      // N transforms. During a resize drag this runs per-pointermove;
      // coalesce to one per frame.
      if (!this._scaleRaf) {
        this._scaleRaf = requestAnimationFrame(() => {
          this._scaleRaf = null;
          this._scaleThumbs();
        });
      }
    }

    /** @page must live in the document stylesheet — it's a no-op inside
     *  shadow DOM. (Re-)append so any author @page landing later in
     *  source order can't reintroduce a margin and push each slide onto
     *  two sheets; called again from beforeprint. */
    _syncPrintPageRule() {
      const id = 'deck-stage-print-page';
      let tag = document.getElementById(id);
      if (!tag) {
        tag = document.createElement('style');
        tag.id = id;
      }
      (document.body || document.head).appendChild(tag);
      tag.textContent = '@page { size: ' + this.designWidth + 'px ' + this.designHeight + 'px; margin: 0; } ' + '@media print { html, body { margin: 0 !important; padding: 0 !important; background: none !important; overflow: visible !important; height: auto !important; } ' + '* { -webkit-print-color-adjust: exact; print-color-adjust: exact; } ' +
      // Jump authored animations/transitions to their end state so print
      // never captures mid-entrance — pairs with the beforeprint handler
      // in connectedCallback that sets data-deck-active on every slide.
      '*, *::before, *::after { animation-delay: -99s !important; animation-duration: .001s !important; ' + 'animation-iteration-count: 1 !important; animation-fill-mode: both !important; ' + 'animation-play-state: running !important; transition-duration: 0s !important; } }';
    }
    _onSlotChange() {
      // Self-mutate path already reconciled synchronously and emitted
      // slidechange; skip the async slotchange it caused.
      if (this._squelchSlotChange) {
        this._squelchSlotChange = false;
        return;
      }
      // Primary lock-clear is the host's __deck_rail_ack; this clears on a
      // dropped ack so the rail can't stay dead.
      this._railLock = false;
      this._collectSlides();
      this._restoreIndex();
      this._applyIndex({
        showOverlay: false,
        broadcast: true,
        reason: 'init'
      });
      this._fit();
    }
    _collectSlides() {
      const assigned = this._slot.assignedElements({
        flatten: true
      });
      this._slides = assigned.filter(el => {
        // Skip template/style/script nodes even if someone slots them.
        const tag = el.tagName;
        return tag !== 'TEMPLATE' && tag !== 'SCRIPT' && tag !== 'STYLE';
      });
      this._slideSet = new Set(this._slides);
      this._slides.forEach((slide, i) => {
        const n = i + 1;
        slide.setAttribute('data-screen-label', `${pad2(n)} ${getSlideLabel(slide)}`);

        // Validation attribute for comment flow / auto-checks.
        if (!slide.hasAttribute('data-om-validate')) {
          slide.setAttribute('data-om-validate', VALIDATE_ATTR);
        }
        slide.setAttribute('data-deck-slide', String(i));
      });
      if (this._totalEl) this._totalEl.textContent = String(this._slides.length || 1);
      if (this._index >= this._slides.length) this._index = Math.max(0, this._slides.length - 1);
      this._markLastVisible();
      this._renderRail();
    }

    /** Tag the last non-skipped slide so print CSS can drop its
     *  break-after (see the @media print comment above — :last-child
     *  alone matches a hidden skipped slide). */
    _markLastVisible() {
      let last = null;
      this._slides.forEach(s => {
        s.removeAttribute('data-deck-last-visible');
        if (!s.hasAttribute('data-deck-skip')) last = s;
      });
      if (last) last.setAttribute('data-deck-last-visible', '');
    }
    _loadNotes() {
      // Per-slide data-speaker-notes is authoritative when present (attrs
      // travel with the element on reorder/dup/delete); a slide without
      // the attr falls through to the legacy #speaker-notes JSON array
      // PER SLIDE so a single attr on a JSON-authored deck doesn't blank
      // the rest.
      const tag = document.getElementById('speaker-notes');
      let json = null;
      if (tag) try {
        const p = JSON.parse(tag.textContent || '[]');
        if (Array.isArray(p)) json = p;
      } catch (e) {
        console.warn('[deck-stage] Failed to parse #speaker-notes JSON:', e);
      }
      this._notes = this._slides.map((s, i) => {
        const a = s.getAttribute('data-speaker-notes');
        return a !== null ? a : json && typeof json[i] === 'string' ? json[i] : '';
      });
    }
    _restoreIndex() {
      // The host's ?slide= param is delivered as a #<int> hash (1-indexed) on
      // the iframe src. No hash → slide 1; the deck itself keeps no position
      // state across loads.
      const h = (location.hash || '').match(/^#(\d+)$/);
      if (h) {
        const n = parseInt(h[1], 10) - 1;
        if (n >= 0 && n < this._slides.length) this._index = n;
      }
    }
    _applyIndex({
      showOverlay = true,
      broadcast = true,
      reason = 'init'
    } = {}) {
      if (!this._slides.length) return;
      const prev = this._prevIndex == null ? -1 : this._prevIndex;
      const curr = this._index;
      // Keep the iframe's own hash in sync so an in-iframe location.reload()
      // (reload banner path in viewer-handle.ts) lands on the current slide,
      // not the stale deep-link hash from initial load.
      try {
        history.replaceState(null, '', '#' + (curr + 1));
      } catch (e) {}
      this._slides.forEach((s, i) => {
        if (i === curr) s.setAttribute('data-deck-active', '');else s.removeAttribute('data-deck-active');
      });
      if (this._countEl) this._countEl.textContent = String(curr + 1);
      // Follow-scroll on every navigation (init deep-link, keyboard, click,
      // tap, external goTo) — the only time we *don't* want the rail to
      // track current is after a rail-internal mutation, where _renderRail
      // has already restored the user's scroll position and yanking back to
      // current would undo it.
      this._syncRail(reason !== 'mutation');
      if (broadcast) {
        // (1) Legacy: host-window postMessage for speaker-notes renderers.
        try {
          window.postMessage({
            slideIndexChanged: curr,
            deckTotal: this._slides.length,
            deckSkipped: this._skippedIndices()
          }, '*');
        } catch (e) {}

        // (2) In-page CustomEvent on the <deck-stage> element itself.
        //     Bubbles and composes out of shadow DOM so slide code can listen:
        //       document.querySelector('deck-stage').addEventListener('slidechange', e => {
        //         e.detail.index, e.detail.previousIndex, e.detail.total, e.detail.slide, e.detail.reason
        //       });
        const detail = {
          index: curr,
          previousIndex: prev,
          total: this._slides.length,
          slide: this._slides[curr] || null,
          previousSlide: prev >= 0 ? this._slides[prev] || null : null,
          reason: reason // 'init' | 'keyboard' | 'click' | 'tap' | 'api'
        };
        this.dispatchEvent(new CustomEvent('slidechange', {
          detail,
          bubbles: true,
          composed: true
        }));
      }
      this._prevIndex = curr;
      if (showOverlay) this._flashOverlay();
    }
    _flashOverlay() {
      // Host posts __omelette_presenting while in fullscreen/tab presentation
      // mode — suppress the nav footer entirely (both hover and slide-change
      // flash) so the audience sees clean slides.
      if (!this._overlay || this._presenting) return;
      this._overlay.setAttribute('data-visible', '');
      if (this._hideTimer) clearTimeout(this._hideTimer);
      this._hideTimer = setTimeout(() => {
        this._overlay.removeAttribute('data-visible');
      }, OVERLAY_HIDE_MS);
    }
    _railWidth() {
      // State-based, no offsetWidth: the first _fit() can run before the
      // rail has had layout on some load paths, and a 0 there paints the
      // slide full-width for one frame before the post-slotchange _fit()
      // corrects it.
      if (!this._railEnabled || !this._railVisible || this.hasAttribute('no-rail') || this.hasAttribute('noscale') || this._presenting || this._previewMode || NARROW_MQ.matches) return 0;
      return this._railPx || 0;
    }
    _fit() {
      if (!this._canvas) return;
      const stage = this._canvas.parentElement;
      // PPTX export sets noscale so the DOM capture sees authored-size
      // geometry — the scaled canvas is in shadow DOM, so the exporter's
      // resetTransformSelector can't reach .canvas.style.transform directly.
      if (this.hasAttribute('noscale')) {
        this._canvas.style.transform = 'none';
        if (stage) stage.style.left = '0';
        if (this._overlay) this._overlay.style.marginLeft = '0';
        return;
      }
      const rw = this._railWidth();
      if (stage) stage.style.left = rw + 'px';
      // Overlay is centred on the viewport via left:50% + translate(-50%);
      // marginLeft shifts the centre by rw/2 so it lands in the middle of
      // the [rw, innerWidth] stage region.
      if (this._overlay) this._overlay.style.marginLeft = rw / 2 + 'px';
      const vw = window.innerWidth - rw;
      const vh = window.innerHeight;
      const s = Math.min(vw / this.designWidth, vh / this.designHeight);
      this._canvas.style.transform = `scale(${s})`;
    }
    _onResize() {
      this._fit();
      // Crossing the narrow-viewport breakpoint reveals the rail — rerun the
      // thumbnail scale the same way _setRailWidth does.
      if (!this._scaleRaf) {
        this._scaleRaf = requestAnimationFrame(() => {
          this._scaleRaf = null;
          this._scaleThumbs();
        });
      }
    }
    _onMouseMove() {
      // Keep overlay visible while mouse moves; hide after idle.
      this._flashOverlay();
    }
    _onMessage(e) {
      const d = e.data;
      if (d && typeof d.__omelette_presenting === 'boolean') {
        this._presenting = d.__omelette_presenting;
        if (this._presenting && this._overlay) {
          this._overlay.removeAttribute('data-visible');
          if (this._hideTimer) clearTimeout(this._hideTimer);
        }
        this._syncRailHidden();
        this._closeMenu();
        this._closeConfirm();
        this._fit();
        this._scaleThumbs();
      }
      // Host's Preview segment (ViewerMode='none'): the rail's drag-reorder /
      // right-click skip-delete affordances are editing chrome, so hide it
      // while the user is just looking at the deck. Same hard-hide path as
      // presenting; independent of the user's _railVisible preference so
      // returning to Edit restores whatever they had.
      if (d && typeof d.__omelette_preview_mode === 'boolean') {
        if (d.__omelette_preview_mode === this._previewMode) return;
        this._previewMode = d.__omelette_preview_mode;
        this._syncRailHidden();
        this._closeMenu();
        this._closeConfirm();
        this._fit();
        this._scaleThumbs();
      }
      // Host has processed a dc-op; rail input is safe again. Not tied to
      // slotchange — setAttr and refusal don't fire one. On refusal,
      // revert the optimistic _index/hash adjustment so the next nav
      // starts from what's actually on screen.
      if (d && d.__dc_op_ack) {
        this._railLock = false;
        if (d.applied === false && this._indexBeforeEmit != null) {
          this._index = this._indexBeforeEmit;
          try {
            history.replaceState(null, '', '#' + (this._index + 1));
          } catch (e) {}
        }
        this._indexBeforeEmit = null;
      }
      // Per-viewer show/hide, driven by the TweaksPanel's auto-injected
      // "Thumbnail rail" toggle (or any author script). Independent of
      // whether the Tweaks panel itself is open — closing the panel
      // doesn't change rail visibility. Persists alongside rail width.
      if (d && d.type === '__deck_rail_visible' && typeof d.on === 'boolean') {
        if (d.on === this._railVisible) return;
        this._railVisible = d.on;
        try {
          localStorage.setItem('deck-stage.railVisible', d.on ? '1' : '0');
        } catch (e) {}
        // Arm the transition, commit it, then flip state — otherwise the
        // browser coalesces both writes and nothing animates on show.
        this.setAttribute('data-rail-anim', '');
        void (this._rail && this._rail.offsetHeight);
        this._syncRailHidden();
        this._fit();
        this._scaleThumbs();
        clearTimeout(this._railAnimTimer);
        this._railAnimTimer = setTimeout(() => this.removeAttribute('data-rail-anim'), 220);
      }
      if (d && d.type === '__omelette_rail_enabled') this._enableRail();
    }
    _syncRailHidden() {
      if (!this._rail) return;
      // data-presenting is the hard hide (display:none) for flag-off,
      // presentation mode, and the host's Preview segment — instant, no
      // transition. data-user-hidden is the soft hide (translateX(-100%))
      // for the viewer's rail toggle, so show/hide slides under
      // :host([data-rail-anim]).
      const hard = !this._railEnabled || this._presenting || this._previewMode;
      if (hard) this._rail.setAttribute('data-presenting', '');else this._rail.removeAttribute('data-presenting');
      if (!this._railVisible) this._rail.setAttribute('data-user-hidden', '');else this._rail.removeAttribute('data-user-hidden');
      // translateX hide leaves thumbs (tabIndex=0) in the tab order —
      // inert keeps them unfocusable while the rail is off-screen.
      this._rail.inert = hard || !this._railVisible;
    }
    _onTap(e) {
      // Touch-only — keyboard + the overlay toolbar cover nav on desktop.
      if (FINE_POINTER_MQ.matches) return;
      // Only taps that land on the stage (slide content or letterbox); the
      // overlay / rail / menus are siblings with their own click handlers.
      const path = e.composedPath();
      if (!this._stage || !path.includes(this._stage)) return;
      // Let interactive slide content keep the tap. composedPath (not
      // e.target.closest) so we see through open shadow roots — a <button>
      // inside a slide-authored custom element retargets e.target to the
      // host but still appears in the composed path.
      if (e.defaultPrevented) return;
      for (const n of path) {
        if (n === this._stage) break;
        if (n.matches && n.matches(INTERACTIVE_SEL)) return;
      }
      e.preventDefault();
      const rw = this._railWidth();
      const mid = rw + (window.innerWidth - rw) / 2;
      this._advance(e.clientX < mid ? -1 : 1, 'tap');
    }
    _onKey(e) {
      // Ignore when the user is typing.
      const t = e.target;
      if (t && (t.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName))) return;
      // Confirm dialog swallows nav keys while open; Escape cancels. Enter
      // is left to the focused button's native activation so Tab→Cancel
      // →Enter activates Cancel, not the window-level confirm path.
      if (this._confirm && this._confirm.hasAttribute('data-open')) {
        if (e.key === 'Escape') {
          this._closeConfirm();
          e.preventDefault();
        }
        return;
      }
      if (e.key === 'Escape' && this._menu && this._menu.hasAttribute('data-open')) {
        this._closeMenu();
        e.preventDefault();
        return;
      }
      if (e.metaKey || e.ctrlKey || e.altKey) return;
      const key = e.key;
      let handled = true;
      if (key === 'ArrowRight' || key === 'PageDown' || key === ' ' || key === 'Spacebar') {
        this._advance(1, 'keyboard');
      } else if (key === 'ArrowLeft' || key === 'PageUp') {
        this._advance(-1, 'keyboard');
      } else if (key === 'Home') {
        this._go(0, 'keyboard');
      } else if (key === 'End') {
        this._go(this._slides.length - 1, 'keyboard');
      } else if (key === 'r' || key === 'R') {
        this._go(0, 'keyboard');
      } else if (/^[0-9]$/.test(key)) {
        // 1..9 jump to that slide; 0 jumps to 10.
        const n = key === '0' ? 9 : parseInt(key, 10) - 1;
        if (n < this._slides.length) this._go(n, 'keyboard');
      } else {
        handled = false;
      }
      if (handled) {
        e.preventDefault();
        this._flashOverlay();
      }
    }
    _go(i, reason = 'api') {
      if (!this._slides.length) return;
      const clamped = Math.max(0, Math.min(this._slides.length - 1, i));
      if (clamped === this._index) {
        this._flashOverlay();
        return;
      }
      this._index = clamped;
      this._applyIndex({
        showOverlay: true,
        broadcast: true,
        reason
      });
    }

    /** Step forward/back skipping any slide marked data-deck-skip. Falls
     *  back to _go's clamp-at-ends behaviour (flash overlay) when there's
     *  nothing further in that direction. */
    _advance(dir, reason) {
      if (!this._slides.length) return;
      let i = this._index + dir;
      while (i >= 0 && i < this._slides.length && this._slides[i].hasAttribute('data-deck-skip')) {
        i += dir;
      }
      if (i < 0 || i >= this._slides.length) {
        this._flashOverlay();
        return;
      }
      this._go(i, reason);
    }

    // ── Thumbnail rail ────────────────────────────────────────────────────
    //
    // Thumbs are keyed by slide element and reused across _renderRail()
    // calls, so a reorder/delete is an O(changed) DOM shuffle instead of an
    // O(N) teardown-and-re-clone. Each thumb starts as a lightweight shell
    // (num + empty frame); the clone is materialized lazily by an
    // IntersectionObserver when the frame scrolls into (or near) view, so
    // only visible-ish slides pay the clone + image-decode cost.

    _renderRail() {
      if (!this._rail || !this._railEnabled) {
        this._thumbs = [];
        return;
      }
      // FLIP: record each *materialized* thumb's top before the reconcile.
      // Off-screen (non-materialized) thumbs don't need the animation and
      // skipping their getBoundingClientRect saves a forced layout per
      // off-screen thumb on large decks.
      const prevTops = new Map();
      (this._thumbs || []).forEach(({
        thumb,
        slide,
        host
      }) => {
        if (host) prevTops.set(slide, thumb.getBoundingClientRect().top);
      });
      const st = this._rail.scrollTop;

      // Reconcile: reuse thumbs that already exist for a slide, create
      // shells for new slides, drop thumbs for removed slides.
      const bySlide = new Map();
      (this._thumbs || []).forEach(t => bySlide.set(t.slide, t));
      const next = [];
      this._slides.forEach(slide => {
        let t = bySlide.get(slide);
        if (t) bySlide.delete(slide);else t = this._makeThumb(slide);
        next.push(t);
      });
      // Orphans — slides removed since last render.
      bySlide.forEach(t => {
        if (this._railObserver) this._railObserver.unobserve(t.frame);
        t.thumb.remove();
      });
      // Put thumbs into document order to match _slides. insertBefore on
      // an already-correctly-placed node is a no-op, so this is cheap
      // when nothing moved.
      next.forEach((t, i) => {
        const want = t.thumb;
        const at = this._rail.children[i];
        if (at !== want) this._rail.insertBefore(want, at || null);
        t.i = i;
        t.num.textContent = String(i + 1);
        if (t.slide.hasAttribute('data-deck-skip')) t.thumb.setAttribute('data-skip', '');else t.thumb.removeAttribute('data-skip');
      });
      this._thumbs = next;
      this._rail.scrollTop = st;
      if (prevTops.size) {
        const moved = [];
        this._thumbs.forEach(({
          thumb,
          slide
        }) => {
          const old = prevTops.get(slide);
          if (old == null) return;
          const dy = old - thumb.getBoundingClientRect().top;
          if (Math.abs(dy) < 1) return;
          thumb.style.transition = 'none';
          thumb.style.transform = `translateY(${dy}px)`;
          moved.push(thumb);
        });
        if (moved.length) {
          // Commit the inverted positions before flipping the transition
          // on — otherwise the browser coalesces both style writes and
          // nothing animates.
          void this._rail.offsetHeight;
          moved.forEach(t => {
            t.style.transition = 'transform 180ms cubic-bezier(.2,.7,.3,1)';
            t.style.transform = '';
          });
          setTimeout(() => moved.forEach(t => {
            t.style.transition = '';
          }), 220);
        }
      }
      requestAnimationFrame(() => this._scaleThumbs());
      this._syncRail(false);
    }

    /** Create a lightweight thumb shell for one slide. The clone is
     *  materialized later by the IntersectionObserver. Event handlers
     *  look up the thumb's *current* index (via _thumbs.indexOf) so the
     *  same element can be reused across reorders. */
    _makeThumb(slide) {
      const thumb = document.createElement('div');
      thumb.className = 'thumb';
      thumb.tabIndex = 0;
      const num = document.createElement('div');
      num.className = 'num';
      const frame = document.createElement('div');
      frame.className = 'frame';
      thumb.append(num, frame);
      const entry = {
        thumb,
        num,
        frame,
        slide,
        clone: null,
        host: null,
        i: -1
      };
      // entry.i is refreshed on every _renderRail reconcile pass, so
      // handlers read the thumb's current position without an O(N) scan.
      const idx = () => entry.i;
      thumb.addEventListener('click', () => this._go(idx(), 'click'));
      // ↑/↓ step through the rail when a thumb has focus. _go clamps at the
      // ends and _applyIndex→_syncRail scrolls the new current thumb into
      // view; we move focus to it (preventScroll — _syncRail already
      // scrolled) so a held key walks the whole list. stopPropagation keeps
      // this out of the window-level _onKey nav handler.
      thumb.addEventListener('keydown', e => {
        if (e.key !== 'ArrowUp' && e.key !== 'ArrowDown') return;
        if (e.metaKey || e.ctrlKey || e.altKey) return;
        e.preventDefault();
        e.stopPropagation();
        this._go(idx() + (e.key === 'ArrowDown' ? 1 : -1), 'keyboard');
        const cur = this._thumbs && this._thumbs[this._index];
        if (cur) cur.thumb.focus({
          preventScroll: true
        });
      });
      thumb.addEventListener('contextmenu', e => {
        e.preventDefault();
        this._openMenu(idx(), e.clientX, e.clientY);
      });
      thumb.draggable = true;
      thumb.addEventListener('dragstart', e => {
        this._dragFrom = idx();
        thumb.setAttribute('data-dragging', '');
        e.dataTransfer.effectAllowed = 'move';
        try {
          e.dataTransfer.setData('text/plain', String(this._dragFrom));
        } catch (err) {}
      });
      thumb.addEventListener('dragend', () => {
        thumb.removeAttribute('data-dragging');
        this._clearDrop();
        this._dragFrom = null;
      });
      thumb.addEventListener('dragover', e => {
        if (this._dragFrom == null) return;
        e.preventDefault();
        e.dataTransfer.dropEffect = 'move';
        const r = thumb.getBoundingClientRect();
        this._setDrop(idx(), e.clientY < r.top + r.height / 2 ? 'before' : 'after');
      });
      thumb.addEventListener('drop', e => {
        if (this._dragFrom == null) return;
        e.preventDefault();
        const i = idx();
        const r = thumb.getBoundingClientRect();
        let to = e.clientY >= r.top + r.height / 2 ? i + 1 : i;
        if (this._dragFrom < to) to--;
        const from = this._dragFrom;
        this._clearDrop();
        this._dragFrom = null;
        if (to !== from) this._moveSlide(from, to);
      });
      if (this._railObserver) this._railObserver.observe(frame);
      frame.__deckThumb = entry;
      return entry;
    }

    /** Lazily build the clone for a thumb that has scrolled into view. */
    _materialize(entry) {
      if (entry.host) return;
      const dw = this.designWidth,
        dh = this.designHeight;
      let clone = entry.slide.cloneNode(true);
      clone.removeAttribute('id');
      clone.removeAttribute('data-deck-active');
      clone.querySelectorAll('[id]').forEach(el => el.removeAttribute('id'));
      // Neuter heavy media; replace <video> with its poster so the box
      // keeps a visual. <iframe>/<audio> become empty placeholders.
      clone.querySelectorAll('iframe, audio, object, embed').forEach(el => {
        el.removeAttribute('src');
        el.removeAttribute('srcdoc');
        el.removeAttribute('data');
        el.innerHTML = '';
      });
      clone.querySelectorAll('video').forEach(el => {
        if (!el.poster) {
          el.removeAttribute('src');
          el.innerHTML = '';
          return;
        }
        const img = document.createElement('img');
        img.src = el.poster;
        img.alt = '';
        img.style.cssText = el.style.cssText + ';object-fit:cover;width:100%;height:100%;';
        img.className = el.className;
        el.replaceWith(img);
      });
      // Images: defer decode and let the browser pick the smallest
      // srcset candidate for the ~140px thumb. Same-URL clones reuse the
      // slide's decoded bitmap (URL-keyed cache), so the remaining cost
      // is paint/composite — lazy+async keeps that off the main thread.
      clone.querySelectorAll('img').forEach(el => {
        el.loading = 'lazy';
        el.decoding = 'async';
        if (el.srcset) el.sizes = (this._railPx || 188) + 'px';
      });
      // Custom elements inside the slide would have their
      // connectedCallback fire when the clone is appended. Replace them
      // with inert boxes so a component-heavy deck doesn't run N copies
      // of each component's mount logic in the rail. Children are
      // preserved so layout-wrapper elements (<my-column><h2>…</h2>)
      // still show their authored content; the querySelectorAll NodeList
      // is static, so nested custom elements in the moved subtree are
      // still visited on later iterations.
      const neuter = el => {
        const box = document.createElement('div');
        box.style.cssText = (el.getAttribute('style') || '') + ';background:rgba(0,0,0,0.06);border:1px dashed rgba(0,0,0,0.15);';
        box.className = el.className;
        // Preserve theming/i18n hooks so [data-*] / :lang() / [dir]
        // descendant selectors still match the neutered root.
        for (const a of el.attributes) {
          const n = a.name;
          if (n.startsWith('data-') || n.startsWith('aria-') || n === 'lang' || n === 'dir' || n === 'role' || n === 'title') {
            box.setAttribute(n, a.value);
          }
        }
        while (el.firstChild) box.appendChild(el.firstChild);
        return box;
      };
      // querySelectorAll('*') returns descendants only — a custom-element
      // slide root (<my-slide>…</my-slide>) would slip through and upgrade
      // on append. Swap the root first.
      if (clone.tagName.includes('-')) clone = neuter(clone);
      clone.querySelectorAll('*').forEach(el => {
        if (el.tagName.includes('-')) el.replaceWith(neuter(el));
      });
      clone.style.cssText += ';position:absolute;top:0;left:0;transform-origin:0 0;' + 'pointer-events:none;width:' + dw + 'px;height:' + dh + 'px;' + 'box-sizing:border-box;overflow:hidden;visibility:visible;opacity:1;';
      const host = document.createElement('div');
      host.style.cssText = 'position:absolute;inset:0;';
      this._syncThumbHostAttrs(host);
      const sr = host.attachShadow({
        mode: 'open'
      });
      if (this._adoptedSheet) sr.adoptedStyleSheets = [this._adoptedSheet];else {
        const st = document.createElement('style');
        st.textContent = this._authorCss || '';
        sr.appendChild(st);
      }
      sr.appendChild(clone);
      entry.frame.appendChild(host);
      entry.host = host;
      entry.clone = clone;
      if (this._thumbScale) clone.style.transform = 'scale(' + this._thumbScale + ')';
      // Once materialized the IO callback is a no-op early-return —
      // unobserve so scroll doesn't keep firing it.
      if (this._railObserver) this._railObserver.unobserve(entry.frame);
    }

    /** Re-clone a single thumb (live-update path). No-op if the thumb
     *  hasn't been materialized yet — it'll pick up current content when
     *  it scrolls into view. */
    _refreshThumb(slide) {
      const entry = (this._thumbs || []).find(t => t.slide === slide);
      if (!entry || !entry.host) return;
      entry.host.remove();
      entry.host = entry.clone = null;
      this._materialize(entry);
    }
    _scaleThumbs() {
      if (!this._thumbs || !this._thumbs.length) return;
      // Every frame is the same width; if it reads 0 the rail is
      // display:none (noscale / no-rail / presenting / print) — leave the
      // clones as-is and re-run when the rail is revealed.
      const fw = this._thumbs[0].frame.offsetWidth;
      if (!fw) return;
      this._thumbScale = fw / this.designWidth;
      this._thumbs.forEach(({
        clone
      }) => {
        if (clone) clone.style.transform = 'scale(' + this._thumbScale + ')';
      });
    }
    _setDrop(i, where) {
      // dragover fires at pointer-event rate; touch only the previous
      // and new target rather than sweeping all N thumbs.
      const t = this._thumbs && this._thumbs[i];
      if (this._dropOn && this._dropOn !== t) {
        this._dropOn.thumb.removeAttribute('data-drop');
      }
      if (t) t.thumb.setAttribute('data-drop', where);
      this._dropOn = t || null;
    }
    _clearDrop() {
      if (this._dropOn) this._dropOn.thumb.removeAttribute('data-drop');
      this._dropOn = null;
    }
    _syncRail(follow) {
      if (!this._thumbs) return;
      this._thumbs.forEach(({
        thumb
      }, i) => {
        if (i === this._index) {
          thumb.setAttribute('data-current', '');
          if (follow && typeof thumb.scrollIntoView === 'function') {
            thumb.scrollIntoView({
              block: 'nearest'
            });
          }
        } else {
          thumb.removeAttribute('data-current');
        }
      });
    }
    _openMenu(i, x, y) {
      if (!this._menu) return;
      this._menuIndex = i;
      const slide = this._slides[i];
      const skip = slide && slide.hasAttribute('data-deck-skip');
      this._menu.querySelector('[data-act="skip"]').textContent = skip ? 'Unskip slide' : 'Skip slide';
      this._menu.querySelector('[data-act="up"]').disabled = i <= 0;
      this._menu.querySelector('[data-act="down"]').disabled = i >= this._slides.length - 1;
      this._menu.querySelector('[data-act="delete"]').disabled = this._slides.length <= 1;
      // Place, then clamp to viewport after it's measurable.
      this._menu.style.left = x + 'px';
      this._menu.style.top = y + 'px';
      this._menu.setAttribute('data-open', '');
      const r = this._menu.getBoundingClientRect();
      const nx = Math.min(x, window.innerWidth - r.width - 4);
      const ny = Math.min(y, window.innerHeight - r.height - 4);
      this._menu.style.left = Math.max(4, nx) + 'px';
      this._menu.style.top = Math.max(4, ny) + 'px';
    }
    _closeMenu() {
      if (this._menu) this._menu.removeAttribute('data-open');
      this._menuIndex = -1;
    }
    _openConfirm(i) {
      if (!this._confirm) return;
      this._confirmIndex = i;
      this._confirm.querySelector('.title').textContent = 'Delete slide ' + (i + 1) + '?';
      this._confirm.setAttribute('data-open', '');
      const btn = this._confirm.querySelector('.danger');
      if (btn && btn.focus) btn.focus();
    }
    _closeConfirm() {
      if (this._confirm) this._confirm.removeAttribute('data-open');
      this._confirmIndex = -1;
    }

    /** Rail mutations. When a dc-runtime is present (`window.__dcUpdate`)
     *  the host owns the light DOM — handlers emit a dc-op only and the
     *  host applies it (to the editor's model or to the source file) and
     *  re-renders via dc-runtime; slotchange catches the rail up.
     *  Structural ops lock rail input until the host acks so a rapid second
     *  click can't address a stale index; setAttr/removeAttr respect the
     *  lock but don't set it (indices unchanged; the host serializes).
     *  `newIndex` is written to location.hash so slotchange's
     *  _restoreIndex lands on the right slide.
     *
     *  With NO dc-runtime (a raw .html deck), there's no re-render path,
     *  so handlers self-mutate locally for an instant update and emit
     *  `emitOnly: false`; the host persists to disk without
     *  re-rendering over the already-mutated DOM.
     *
     *  See docs/dc-ops.md for the contract. */
    _emitDcOp(op, slide, lock, newIndex) {
      // Slide index (template/script/style filtered — same as
      // _collectSlides). deck-stage is a filtered-index dc-op emitter;
      // the host resolves against findDeckStage().slideTids. Callers
      // already pass `to` as a slide index.
      op.at = this._slides.indexOf(slide);
      op.witness = {
        childCount: this._slides.length
      };
      // dc-runtime wraps an <x-import>-mounted component in a
      // <div class="sc-host-x" data-dc-tpl="N"> host — the stamp is on the
      // WRAPPER, not this element. closest() finds it (or this element's
      // own stamp when directly templated).
      const host = this.closest('[data-dc-tpl]');
      const tid = host && host.getAttribute('data-dc-tpl');
      op.mount = {
        tid: tid !== null ? parseInt(tid, 10) : null,
        tag: 'deck-stage'
      };
      op.emitOnly = !!window.__dcUpdate;
      if (op.emitOnly) {
        if (lock) this._railLock = true;
        if (newIndex != null && newIndex !== this._index) {
          this._indexBeforeEmit = this._index;
          this._index = newIndex;
          try {
            history.replaceState(null, '', '#' + (newIndex + 1));
          } catch (e) {}
        }
      }
      this.dispatchEvent(new CustomEvent('dc-op', {
        detail: op,
        bubbles: true,
        composed: true
      }));
      return op.emitOnly;
    }
    _deleteSlide(i) {
      if (this._railLock) return;
      const slide = this._slides[i];
      if (!slide || this._slides.length <= 1) return;
      const cur = this._index;
      const ni = i < cur || i === cur && i === this._slides.length - 1 ? cur - 1 : cur;
      if (this._emitDcOp({
        op: 'remove'
      }, slide, true, ni)) return;
      this._index = ni;
      this._squelchSlotChange = true;
      slide.remove();
      this._collectSlides();
      this._applyIndex({
        showOverlay: true,
        broadcast: true,
        reason: 'mutation'
      });
    }
    _duplicateSlide(i) {
      if (this._railLock) return;
      const slide = this._slides[i];
      if (!slide) return;
      if (this._emitDcOp({
        op: 'duplicate'
      }, slide, true, i + 1)) return;
      const copy = slide.cloneNode(true);
      copy.removeAttribute('id');
      copy.querySelectorAll('[id]').forEach(el => el.removeAttribute('id'));
      this._index = i + 1;
      this._squelchSlotChange = true;
      this.insertBefore(copy, slide.nextSibling);
      this._collectSlides();
      this._applyIndex({
        showOverlay: true,
        broadcast: true,
        reason: 'mutation'
      });
    }
    _toggleSkip(i) {
      if (this._railLock) return;
      const slide = this._slides[i];
      if (!slide) return;
      const on = !slide.hasAttribute('data-deck-skip');
      if (this._emitDcOp(on ? {
        op: 'setAttr',
        attr: 'data-deck-skip',
        value: ''
      } : {
        op: 'removeAttr',
        attr: 'data-deck-skip'
      }, slide, false)) return;
      if (on) slide.setAttribute('data-deck-skip', '');else slide.removeAttribute('data-deck-skip');
    }
    _skippedIndices() {
      const out = [];
      for (let i = 0; i < this._slides.length; i++) {
        if (this._slides[i].hasAttribute('data-deck-skip')) out.push(i);
      }
      return out;
    }
    _moveSlide(i, j) {
      if (this._railLock || j < 0 || j >= this._slides.length || j === i) return;
      const cur = this._index;
      const ni = cur === i ? j : i < cur && j >= cur ? cur - 1 : i > cur && j <= cur ? cur + 1 : cur;
      const slide = this._slides[i];
      if (this._emitDcOp({
        op: 'move',
        to: j
      }, slide, true, ni)) return;
      const ref = j < i ? this._slides[j] : this._slides[j].nextSibling;
      this._index = ni;
      this._squelchSlotChange = true;
      this.insertBefore(slide, ref);
      this._collectSlides();
      this._applyIndex({
        showOverlay: false,
        broadcast: true,
        reason: 'mutation'
      });
    }

    // Public API ------------------------------------------------------------

    /** Current slide index (0-based). */
    get index() {
      return this._index;
    }
    /** Total slide count. */
    get length() {
      return this._slides.length;
    }
    /** Programmatically navigate. */
    goTo(i) {
      this._go(i, 'api');
    }
    next() {
      this._advance(1, 'api');
    }
    prev() {
      this._advance(-1, 'api');
    }
    reset() {
      this._go(0, 'api');
    }
  }
  if (!customElements.get('deck-stage')) {
    customElements.define('deck-stage', DeckStage);
  }
})();
})(); } catch (e) { __ds_ns.__errors.push({ path: "deck/deck-stage.js", error: String((e && e.message) || e) }); }

// ui_kits/clockwork-scene/GameScene.jsx
try { (() => {
/* GameScene — interactive recreation of The Clockwork Dark scene.
   "Lit by tallow and mistrust": a cold, grim Ash & Thorn frame —
   slate shadow and bleak air — with a slight tinker-brass accent and
   the journal glowing as the one warm, lit thing. Composes the DS
   components with a faked turn loop and a phase switcher.
   Globals (bundle): Button, ChoiceChip, Badge, StatLine,
   AssistantBubble, DiceToast, ScenePanel, WorldClock. */

const NS = window.TheClockworkDarkDesignSystem_4a0a88;
const {
  Button,
  ChoiceChip,
  Badge,
  StatLine,
  AssistantBubble,
  DiceToast,
  ScenePanel,
  WorldClock
} = NS;
const {
  useState,
  useRef,
  useEffect
} = React;

// ---- Fake content (drawn from data/lore + economy) ----
// Each choice may carry `to` (navigate to a scene) and/or `say` (a flavor
// beat that stays in place). Navigation is data-driven off `to`.
const SCENES = {
  forest_clearing: {
    title: "The Forest Clearing",
    caption: "Birch margin · dawn mist",
    img: "../../assets/art/scenes/forest-mushroom-ring.jpg",
    tint: "radial-gradient(120% 78% at 52% 6%, rgba(214,178,108,.22), transparent 48%), linear-gradient(178deg,#10171a 0%,#18211d 42%,#26302a 74%,#34392e 100%)",
    narration: "You wake where the birch gives way to fern. Mushroom circles, game trails that double back when watched. Smoke from Edgewood drifts west — even though the wind blows south.",
    choices: [{
      id: "smoke",
      text: "Walk toward the smoke",
      to: "edgewood_square"
    }, {
      id: "forage",
      text: "Forage the clearing",
      say: "Herbs, resin, and clay come up easy. Something watches from stillness without moving — you gather what you can and do not look twice."
    }, {
      id: "listen",
      text: "Listen",
      say: "Under the birds, a fainter sound: a tick, slow and even, that does not belong to any clock you can see."
    }],
    assistant: {
      form: "cat",
      text: "The smoke is bread, not burning. Probably."
    }
  },
  edgewood_square: {
    title: "Edgewood Square",
    caption: "Communal oven · failing light",
    img: "../../assets/art/scenes/town-scene.jpg",
    tint: "radial-gradient(100% 76% at 64% 12%, rgba(214,150,80,.26), transparent 46%), linear-gradient(178deg,#10161a 0%,#1b2020 44%,#33291d 80%,#43321f 100%)",
    narration: "Timber frames lean together around the communal oven. A shrine to unnamed saints keeps its candle. Maris hums at the bakery door, flour on her sleeves — villagers say she hums to keep the gears quiet.",
    choices: [{
      id: "bakery",
      text: "Visit Maris at the bakery",
      to: "edgewood_bakery"
    }, {
      id: "shrine",
      text: "Cross to the shrine",
      to: "edgewood_shrine"
    }, {
      id: "caravan",
      text: "Find Ilya's caravan",
      to: "tinker_caravan"
    }, {
      id: "board",
      text: "Read the notice board",
      say: "Fresh nails on the militia board. Below them, in a child's hand: gears, drawn and half rubbed out. Odran swears the road to Millhaven took an extra hour though the sun said otherwise."
    }],
    assistant: {
      form: "cat",
      text: "Stay near the oven light. It is honest."
    }
  },
  edgewood_bakery: {
    title: "The Hearth Bakery",
    caption: "Brick oven · morning prep",
    img: "../../assets/art/scenes/bakery.jpg",
    tint: "radial-gradient(90% 86% at 32% 56%, rgba(214,150,80,.40), transparent 58%), linear-gradient(178deg,#1a120c 0%,#2c1c12 46%,#4a2f1a 80%,#6b4524 100%)",
    narration: "Warm dark and the smell of crust. Maris Hearth works the loaves without looking up, humming low. Flour hangs in the oven light. A cooling loaf sits apart from the others, untouched.",
    choices: [{
      id: "buy",
      text: "Buy a loaf (2c)",
      say: "Maris wraps it in cloth, warm through. \"Eat it honest,\" she says. \"Not all bread is.\" Her eyes flick, once, to the loaf set apart."
    }, {
      id: "ring",
      text: "Ask about the loaf set apart",
      say: "She stops humming. \"It rang,\" she says, \"when it cracked. Like a bell.\" She does not throw it out, and she does not say why."
    }, {
      id: "back",
      text: "Back to the square",
      to: "edgewood_square"
    }],
    assistant: {
      form: "cat",
      text: "She hums on the off-beat now. As if answering something."
    }
  },
  edgewood_shrine: {
    title: "Shrine of Unnamed Saints",
    caption: "Candle wall · the unfinished mural",
    tint: "radial-gradient(80% 80% at 50% 64%, rgba(214,178,108,.30), transparent 60%), linear-gradient(178deg,#150f0a 0%,#241c12 48%,#3c2e1c 80%,#5a4630 100%)",
    narration: "Votive candles gutter along a wall that nobody can finish. Saints with missing faces. Wheat threaded with brass. A road winding inward toward a wound of light. Greta Moss tends the flames and watches you watch the wall.",
    choices: [{
      id: "mural",
      text: "Study the mural",
      say: "The unfinished edge shows a child offering bread to something underground. The brass in the painted wheat catches your candle and seems, for a breath, to turn."
    }, {
      id: "ask",
      text: "Ask Greta why it's unfinished",
      say: "\"Finishing it,\" she says, not looking from the candles, \"would invite the road to arrive. Some walls are kinder left half-told.\""
    }, {
      id: "back",
      text: "Back to the square",
      to: "edgewood_square"
    }],
    assistant: {
      form: "child",
      text: "I helped with the gears. She drew them wrong. I can show you right."
    }
  },
  tinker_caravan: {
    title: "The Tinker Caravan",
    caption: "Nine-pin tent · last of the dusk",
    img: "../../assets/art/scenes/tinker-cart.jpg",
    tint: "radial-gradient(110% 78% at 50% 20%, rgba(190,118,58,.28), transparent 50%), linear-gradient(178deg,#12120f 0%,#241a13 46%,#3c2818 80%,#553a22 100%)",
    narration: "Nine brass pins glint in Ilya's scarf. Charms hang from the tent ribs; chalk symbols mark roads that shift when the wheat turns wrong. A sympathy lamp burns with no flame you can name.",
    choices: [{
      id: "barter",
      text: "Barter for a sympathy charm",
      say: "Ilya weighs your forage in one palm, the charm in the other. \"It works,\" they say, \"or it reassures. Both are worth copper out here.\""
    }, {
      id: "map",
      text: "Buy the road to Millhaven",
      to: "millhaven_gate"
    }, {
      id: "leave",
      text: "Step back into the dusk",
      to: "edgewood_square"
    }],
    assistant: {
      form: "tinker",
      text: "Ilya counts you twice. Once for now. Once for later."
    }
  },
  millhaven_gate: {
    title: "Millhaven Gate",
    caption: "Palisade · cold rain",
    img: "../../assets/art/scenes/closing-town-gates.jpg",
    tint: "radial-gradient(120% 84% at 50% 14%, rgba(150,166,170,.22), transparent 54%), linear-gradient(178deg,#0c1114 0%,#161e22 46%,#283238 80%,#39434a 100%)",
    narration: "The road from the caravan runs longer than it should. Rain off the palisade banners, mud thick with refugee tracks. Sergeant Sera Venn holds the gate, scar pale in the lantern light. \"The road from the Heartlands is wrong tonight,\" she says.",
    choices: [{
      id: "showmap",
      text: "Show your road map",
      say: "She studies Ilya's chalk lines, then the dark behind you. \"This road's a day old and already wrong. Keep it close. Don't trust the milestones.\""
    }, {
      id: "watch",
      text: "Offer to stand the watch",
      say: "\"Hungry mouths I can admit,\" she says. \"Brass I cannot. If anything at the gate rings when it shouldn't — you sound the bell, not your conscience.\""
    }, {
      id: "ask",
      text: "Ask what she saw",
      say: "\"Wheat,\" she says, after a while. \"Standing in rows too straight for wind. Marching, almost. I'd call it nerves, but the wheat doesn't have any.\""
    }],
    assistant: {
      form: "wanderer",
      text: "She is not lying. That is what frightens her."
    }
  }
};
const ORDER = ["forest_clearing", "edgewood_square", "edgewood_bakery", "edgewood_shrine", "tinker_caravan", "millhaven_gate"];
const PHASES = ["dormant", "stirring", "spreading", "consuming"];
function SceneVisual({
  scene,
  phase
}) {
  const wrong = phase === "spreading" || phase === "consuming";
  return /*#__PURE__*/React.createElement("div", {
    style: {
      position: "relative",
      height: "min(38vh, 300px)",
      minHeight: 190,
      background: scene.tint,
      overflow: "hidden",
      borderBottom: "1px solid rgba(214,178,108,.22)"
    }
  }, scene.img && /*#__PURE__*/React.createElement("div", {
    key: scene.img,
    className: "cw-cross",
    style: {
      position: "absolute",
      inset: 0,
      backgroundImage: `url("${window.RES(scene.img)}")`,
      backgroundSize: "cover",
      backgroundPosition: "center",
      filter: wrong ? "saturate(.85)" : "none"
    }
  }), /*#__PURE__*/React.createElement("div", {
    className: "cw-flicker",
    style: {
      position: "absolute",
      inset: 0,
      background: "radial-gradient(54% 46% at 52% 14%, rgba(214,178,108,.24), transparent 62%)",
      mixBlendMode: "screen"
    }
  }), wrong && /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      inset: 0,
      background: "var(--corruption)",
      opacity: phase === "consuming" ? 0.28 : 0.15,
      mixBlendMode: "color"
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      inset: 0,
      backgroundImage: "var(--texture-paper)",
      opacity: 0.62,
      mixBlendMode: "multiply"
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      inset: 0,
      boxShadow: "inset 0 0 140px 30px rgba(6,9,9,.86)"
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      top: 0,
      left: 0,
      right: 0,
      height: 30,
      background: "linear-gradient(180deg, rgba(6,9,9,.9), transparent)"
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      bottom: 0,
      left: 0,
      right: 0,
      height: 56,
      background: "linear-gradient(0deg, rgba(6,9,9,.75), transparent)"
    }
  }), /*#__PURE__*/React.createElement("span", {
    style: {
      position: "absolute",
      top: 9,
      right: 13,
      fontFamily: "var(--font-mono)",
      fontSize: 10,
      letterSpacing: ".12em",
      textTransform: "uppercase",
      color: "rgba(214,178,108,.42)"
    }
  }, "ComfyUI still \xB7 ", scene.title), /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      left: 15,
      bottom: 13,
      display: "flex",
      gap: 8,
      alignItems: "center"
    }
  }, /*#__PURE__*/React.createElement(Badge, {
    tone: "candle",
    style: {
      background: "rgba(14,16,12,.6)",
      color: "var(--tallow-300)",
      borderColor: "var(--tallow-700)"
    }
  }, scene.caption), wrong && /*#__PURE__*/React.createElement(Badge, {
    tone: "corruption",
    style: {
      background: "rgba(16,20,8,.6)"
    }
  }, "Wrong rain")));
}
function GameScene() {
  const [started, setStarted] = useState(false);
  const [archetype, setArchetype] = useState("wayfarer");
  const [sceneId, setSceneId] = useState("forest_clearing");
  const [phase, setPhase] = useState("stirring");
  const [log, setLog] = useState([]);
  const [busy, setBusy] = useState(false);
  const [assistantOpen, setAssistantOpen] = useState(false);
  const [toast, setToast] = useState(null);
  const [introOpen, setIntroOpen] = useState(false);
  const [stats, setStats] = useState({
    hp: "18/18",
    stamina: 6,
    gold: "0.00",
    day: 11,
    time: "Dusk"
  });
  const [input, setInput] = useState("");
  const logRef = useRef(null);
  const scene = SCENES[sceneId];
  useEffect(() => {
    if (logRef.current) logRef.current.scrollTop = logRef.current.scrollHeight;
  }, [log]);
  function begin() {
    setStarted(true);
    setLog([{
      kind: "narration",
      text: scene.narration
    }]);
    setTimeout(() => setAssistantOpen(true), 600);
  }
  function rollDice() {
    const roll = 1 + Math.floor(Math.random() * 20);
    const mod = 2,
      dc = 13;
    const outcome = roll === 20 ? "Boon" : roll === 1 ? "Complication" : roll + mod >= dc ? "Success" : "Failure";
    setToast({
      roll,
      modifier: mod,
      dc,
      outcome
    });
    setTimeout(() => setToast(null), 1500);
    return outcome;
  }
  function choose(choice) {
    if (busy) return;
    setBusy(true);
    setLog(l => [...l, {
      kind: "player",
      text: choice.text
    }]);
    const outcome = rollDice();
    setTimeout(() => {
      const moving = !!choice.to && choice.to !== sceneId;
      const tail = outcome === "Failure" ? " You slip — the moment costs you a breath of stamina." : outcome === "Boon" ? " Something others missed catches your eye. A free clue." : "";
      // A `to` choice arrives at a new scene's narration; a `say` choice is a
      // beat in place. Custom typed actions fall back to the current scene.
      const body = choice.to ? SCENES[choice.to].narration : choice.say || scene.narration;
      setLog(l => [...l, {
        kind: "narration",
        text: body + tail
      }]);
      setStats(s => ({
        ...s,
        stamina: Math.max(0, s.stamina - (outcome === "Failure" ? 1 : 0)),
        time: s.time === "Dusk" ? "Night" : s.time === "Night" ? "Deep night" : "Dusk",
        gold: choice.id === "buy" ? Math.max(0, parseFloat(s.gold) - 0.02).toFixed(2) : s.gold,
        day: moving ? s.day + 1 : s.day
      }));
      if (moving) {
        setSceneId(choice.to);
        setAssistantOpen(false);
        setTimeout(() => setAssistantOpen(true), 700);
      }
      setBusy(false);
    }, 700);
  }
  function sendCustom(e) {
    e.preventDefault();
    const t = input.trim();
    if (!t || busy) return;
    setInput("");
    choose({
      id: "custom",
      text: t
    });
  }

  // ---- Start screen ----
  if (!started) {
    const archetypes = [{
      id: "wayfarer",
      name: "Wayfarer",
      note: "Cloak, staff, road boots"
    }, {
      id: "hearthkeeper",
      name: "Hearthkeeper",
      note: "Apron, flour, warm colors"
    }, {
      id: "tinker",
      name: "Tinker-apprentice",
      note: "Tool belt, brass pins, chalk"
    }];
    return /*#__PURE__*/React.createElement("div", {
      "data-phase": phase,
      style: frameStyle
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        position: "absolute",
        inset: 0,
        backgroundImage: `url("${window.RES('../../assets/art/menu-screen.jpg')}")`,
        backgroundSize: "cover",
        backgroundPosition: "center"
      }
    }), /*#__PURE__*/React.createElement("div", {
      style: {
        position: "absolute",
        inset: 0,
        background: "radial-gradient(120% 100% at 50% 30%, rgba(6,8,6,.34), rgba(5,7,5,.82) 96%)"
      }
    }), /*#__PURE__*/React.createElement(Atmosphere, null), /*#__PURE__*/React.createElement("div", {
      style: {
        position: "relative",
        flex: 1,
        display: "grid",
        placeItems: "center",
        padding: 24,
        zIndex: 1
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        width: 470,
        background: "linear-gradient(168deg, rgba(29,33,25,.94) 0%, rgba(16,18,14,.96) 100%)",
        backdropFilter: "blur(2px)",
        padding: "34px 36px",
        borderRadius: 3,
        boxShadow: "0 0 0 1px rgba(214,178,108,.22), 0 34px 90px -22px rgba(0,0,0,.92), 0 0 130px -8px rgba(214,178,108,.12)",
        borderTop: "1px solid rgba(214,178,108,.14)",
        borderLeft: "var(--border-mark) solid var(--rust-clock)"
      }
    }, /*#__PURE__*/React.createElement("img", {
      src: window.RES("../../assets/wordmark.svg"),
      alt: "The Clockwork Dark",
      style: {
        width: 300,
        marginBottom: 18,
        filter: "drop-shadow(0 2px 12px rgba(0,0,0,.6))"
      }
    }), /*#__PURE__*/React.createElement("p", {
      style: {
        fontFamily: "var(--font-narration)",
        fontSize: "var(--text-lg)",
        lineHeight: "var(--leading-relaxed)",
        color: "var(--text-narration)",
        margin: "0 0 22px"
      }
    }, "You wake at the margin of an old forest, the last comfortable village a smudge of smoke to the west. The roads have begun to change when no one is watching. Choose how you came to be here."), /*#__PURE__*/React.createElement("p", {
      style: smallcaps
    }, "Traveler"), /*#__PURE__*/React.createElement("div", {
      style: {
        display: "flex",
        flexDirection: "column",
        gap: 8,
        marginBottom: 22
      }
    }, archetypes.map(a => /*#__PURE__*/React.createElement("button", {
      key: a.id,
      onClick: () => setArchetype(a.id),
      style: {
        textAlign: "left",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        padding: "11px 14px",
        cursor: "pointer",
        fontFamily: "var(--font-ui)",
        background: archetype === a.id ? "rgba(214,178,108,.14)" : "rgba(255,255,255,.03)",
        border: archetype === a.id ? "var(--border-rule) solid var(--rust-clock)" : "var(--border-rule) solid rgba(214,178,108,.16)",
        borderRadius: "var(--radius-sm)",
        boxShadow: archetype === a.id ? "var(--glow-candle)" : "none",
        transition: "all var(--dur-fast) var(--ease-quiet)"
      }
    }, /*#__PURE__*/React.createElement("span", {
      style: {
        fontWeight: 600,
        color: "var(--text-on-dark)"
      }
    }, a.name), /*#__PURE__*/React.createElement("span", {
      style: {
        fontSize: "var(--text-sm)",
        color: "var(--text-muted)"
      }
    }, a.note)))), /*#__PURE__*/React.createElement("div", {
      style: {
        display: "flex",
        gap: 10
      }
    }, /*#__PURE__*/React.createElement(Button, {
      variant: "primary",
      size: "lg",
      onClick: begin,
      style: {
        flex: 1,
        justifyContent: "center"
      }
    }, "Step into the clearing"), /*#__PURE__*/React.createElement(Button, {
      variant: "secondary",
      size: "lg",
      onClick: () => setIntroOpen(true),
      style: {
        justifyContent: "center"
      }
    }, "Watch the intro")))), introOpen && /*#__PURE__*/React.createElement("div", {
      style: {
        position: "absolute",
        inset: 0,
        zIndex: 10,
        background: "#000",
        display: "grid",
        placeItems: "center"
      }
    }, /*#__PURE__*/React.createElement("video", {
      src: window.RES('../../assets/video/intro.mp4'),
      poster: window.RES('../../assets/art/menu-screen.jpg'),
      autoPlay: true,
      controls: true,
      playsInline: true,
      onEnded: () => setIntroOpen(false),
      style: {
        width: "100%",
        height: "100%",
        objectFit: "contain"
      }
    }), /*#__PURE__*/React.createElement("button", {
      onClick: () => setIntroOpen(false),
      style: {
        position: "absolute",
        top: 16,
        right: 18,
        fontFamily: "var(--font-ui)",
        fontSize: "var(--text-sm)",
        padding: "6px 16px",
        borderRadius: "var(--radius-sm)",
        cursor: "pointer",
        color: "var(--text-candlelight)",
        background: "rgba(12,14,10,.7)",
        border: "1px solid rgba(214,178,108,.35)",
        letterSpacing: ".04em"
      }
    }, "Skip \u23CE")));
  }

  // ---- Scene ----
  return /*#__PURE__*/React.createElement("div", {
    "data-phase": phase,
    style: frameStyle
  }, /*#__PURE__*/React.createElement(Atmosphere, null), /*#__PURE__*/React.createElement("header", {
    style: {
      position: "relative",
      display: "flex",
      justifyContent: "space-between",
      alignItems: "center",
      padding: "11px 20px",
      background: "linear-gradient(180deg,#090d0e,#0f1210)",
      borderBottom: "1px solid rgba(214,178,108,.2)",
      boxShadow: "0 2px 16px rgba(0,0,0,.7)",
      zIndex: 2
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "center",
      gap: 11
    }
  }, /*#__PURE__*/React.createElement("img", {
    src: window.RES("../../assets/gear-motif.svg"),
    alt: "",
    className: "cw-turn",
    style: {
      width: 22,
      opacity: 0.92,
      filter: "brightness(1.3) drop-shadow(0 0 8px rgba(190,118,58,.5))"
    }
  }), /*#__PURE__*/React.createElement("h1", {
    style: {
      margin: 0,
      color: "var(--text-on-dark)",
      fontFamily: "var(--font-ui)",
      fontSize: "var(--text-base)",
      fontWeight: 600,
      textTransform: "uppercase",
      letterSpacing: "var(--tracking-title)"
    }
  }, scene.title)), /*#__PURE__*/React.createElement(WorldClock, {
    day: stats.day,
    time: stats.time,
    discovered: phase !== "dormant"
  })), /*#__PURE__*/React.createElement("main", {
    style: {
      position: "relative",
      flex: 1,
      display: "grid",
      gridTemplateColumns: "var(--col-assistant) 1fr var(--col-sheet)",
      minHeight: 0,
      zIndex: 1
    }
  }, /*#__PURE__*/React.createElement(ScenePanel, {
    surface: "panel",
    edge: "right",
    style: {
      display: "flex",
      flexDirection: "column",
      background: "linear-gradient(180deg, #1a2220 0%, #10150f 100%)",
      borderRight: "1px solid rgba(214,178,108,.13)",
      boxShadow: "inset -18px 0 32px -26px #000"
    }
  }, /*#__PURE__*/React.createElement("p", {
    style: {
      ...smallcaps,
      color: "var(--tallow-300)"
    }
  }, "Assistant"), /*#__PURE__*/React.createElement(AssistantBubble, {
    form: scene.assistant.form,
    hidden: !assistantOpen,
    style: {
      boxShadow: "var(--shadow-raise), 0 0 30px -6px rgba(214,178,108,.42)"
    }
  }, scene.assistant.text), /*#__PURE__*/React.createElement("div", {
    style: {
      flex: 1
    }
  }), /*#__PURE__*/React.createElement("p", {
    style: {
      fontFamily: "var(--font-narration)",
      fontStyle: "italic",
      fontSize: "var(--text-sm)",
      color: "rgba(214,210,190,.34)",
      margin: 0,
      lineHeight: 1.45
    }
  }, "Something watches from the stillness without moving.")), /*#__PURE__*/React.createElement("section", {
    style: {
      display: "flex",
      flexDirection: "column",
      minHeight: 0,
      background: "#0a0d0a",
      boxShadow: "0 0 100px -12px rgba(214,178,108,.14)"
    }
  }, /*#__PURE__*/React.createElement(SceneVisual, {
    scene: scene,
    phase: phase
  }), /*#__PURE__*/React.createElement("div", {
    ref: logRef,
    className: "cw-log",
    style: {
      position: "relative",
      flex: 1,
      overflowY: "auto",
      overflowX: "hidden",
      padding: "22px 26px",
      minHeight: 0,
      background: "linear-gradient(180deg, #1c2019 0%, #14160f 100%)",
      backgroundImage: "var(--texture-paper)",
      boxShadow: "inset 0 18px 26px -20px rgba(0,0,0,.7), inset 0 -18px 26px -20px rgba(0,0,0,.6)"
    }
  }, log.map((entry, i) => entry.kind === "narration" ? /*#__PURE__*/React.createElement("p", {
    key: i,
    style: {
      fontFamily: "var(--font-narration)",
      fontSize: "var(--text-lg)",
      lineHeight: "var(--leading-relaxed)",
      color: "var(--text-narration)",
      margin: "0 0 16px",
      textWrap: "pretty"
    }
  }, entry.text) : /*#__PURE__*/React.createElement("p", {
    key: i,
    style: {
      fontFamily: "var(--font-ui)",
      fontSize: "var(--text-sm)",
      fontStyle: "italic",
      color: "var(--accent-candle)",
      margin: "0 0 16px",
      paddingLeft: 12,
      borderLeft: "var(--border-mark) solid var(--rust-500)"
    }
  }, "You chose: ", entry.text))), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      flexWrap: "wrap",
      gap: 8,
      padding: "14px 26px 12px",
      background: "#0d100d",
      borderTop: "1px solid rgba(214,178,108,.13)"
    }
  }, scene.choices.map((c, i) => /*#__PURE__*/React.createElement(ChoiceChip, {
    key: c.id,
    index: i + 1,
    disabled: busy,
    onClick: () => choose(c),
    style: {
      boxShadow: "0 3px 12px -3px rgba(0,0,0,.6)"
    }
  }, c.text))), /*#__PURE__*/React.createElement("form", {
    onSubmit: sendCustom,
    style: {
      display: "flex",
      gap: 8,
      padding: "0 26px 16px 26px",
      background: "#0d100d"
    }
  }, /*#__PURE__*/React.createElement("input", {
    value: input,
    onChange: e => setInput(e.target.value),
    placeholder: "Or type an action\u2026",
    style: {
      flex: 1,
      padding: "10px 12px",
      border: "var(--border-hair) solid #2f342c",
      borderRadius: "var(--radius-sm)",
      fontFamily: "var(--font-ui)",
      fontSize: "var(--text-base)",
      background: "#161a14",
      color: "var(--text-on-dark)"
    }
  }), /*#__PURE__*/React.createElement(Button, {
    variant: "primary",
    type: "submit",
    disabled: busy
  }, "Send"))), /*#__PURE__*/React.createElement(ScenePanel, {
    title: null,
    surface: "ledger",
    edge: "left",
    style: {
      background: "linear-gradient(180deg, #181811 0%, #12120b 100%)",
      borderLeft: "1px solid rgba(214,178,108,.13)",
      boxShadow: "inset 18px 0 32px -26px #000"
    }
  }, /*#__PURE__*/React.createElement("p", {
    style: {
      ...smallcaps,
      color: "var(--tallow-300)"
    }
  }, "Traveler"), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement(DarkStat, {
    label: "HP",
    value: stats.hp
  }), /*#__PURE__*/React.createElement(DarkStat, {
    label: "Stamina",
    value: stats.stamina
  }), /*#__PURE__*/React.createElement(DarkStat, {
    label: "Gold",
    value: stats.gold,
    accent: true
  }), /*#__PURE__*/React.createElement(DarkStat, {
    label: "Location",
    value: sceneId.replace(/_/g, " ")
  })), /*#__PURE__*/React.createElement("p", {
    style: {
      ...smallcaps,
      color: "var(--tallow-300)",
      marginTop: 18
    }
  }, "Inventory"), /*#__PURE__*/React.createElement("ul", {
    style: {
      listStyle: "none",
      padding: 0,
      margin: 0,
      display: "flex",
      flexDirection: "column",
      gap: 7
    }
  }, ["Loaf of bread ×1", "Whetstone ×1", "Wild mushroom ×3", "Tallow candle ×2"].map(it => /*#__PURE__*/React.createElement("li", {
    key: it,
    style: {
      fontFamily: "var(--font-mono)",
      fontSize: "var(--text-sm)",
      color: "var(--linen-300)"
    }
  }, it))))), /*#__PURE__*/React.createElement("footer", {
    style: {
      position: "relative",
      display: "flex",
      alignItems: "center",
      gap: 16,
      padding: "9px 20px",
      background: "linear-gradient(0deg,#090d0e,#0f1210)",
      color: "var(--text-on-dark)",
      fontSize: "var(--text-sm)",
      borderTop: "1px solid rgba(214,178,108,.2)",
      zIndex: 2
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: "var(--font-mono)",
      color: "var(--text-candlelight)"
    }
  }, "Day ", stats.day, " \xB7 ", stats.time, " \xB7 ", phase === "spreading" || phase === "consuming" ? "Wrong rain" : "Overcast"), /*#__PURE__*/React.createElement("span", {
    style: {
      flex: 1
    }
  }), /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: "var(--text-xs)",
      color: "var(--text-muted)",
      textTransform: "uppercase",
      letterSpacing: "var(--tracking-label)"
    }
  }, "Evil phase"), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      gap: 4
    }
  }, PHASES.map(p => /*#__PURE__*/React.createElement("button", {
    key: p,
    onClick: () => setPhase(p),
    title: p,
    style: {
      fontFamily: "var(--font-ui)",
      fontSize: "var(--text-xs)",
      textTransform: "capitalize",
      padding: "4px 10px",
      cursor: "pointer",
      borderRadius: "var(--radius-sm)",
      border: "1px solid " + (phase === p ? "var(--accent-candle)" : "#2f342c"),
      background: phase === p ? "rgba(214,178,108,.18)" : "transparent",
      color: phase === p ? "var(--text-candlelight)" : "var(--text-muted)",
      boxShadow: phase === p ? "0 0 14px -4px rgba(214,178,108,.6)" : "none",
      transition: "all var(--dur-fast) var(--ease-quiet)"
    }
  }, p)))), toast && /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      inset: 0,
      display: "grid",
      placeItems: "center",
      pointerEvents: "none",
      zIndex: 5
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "cw-toast",
    style: {
      filter: "drop-shadow(0 14px 34px rgba(0,0,0,.7))"
    }
  }, /*#__PURE__*/React.createElement(DiceToast, toast))));
}
function DarkStat({
  label,
  value,
  accent
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      justifyContent: "space-between",
      alignItems: "baseline",
      padding: "5px 0",
      borderBottom: "1px solid rgba(214,178,108,.13)"
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: "var(--font-ui)",
      fontSize: "var(--text-xs)",
      textTransform: "uppercase",
      letterSpacing: "var(--tracking-label)",
      color: "rgba(214,206,184,.58)"
    }
  }, label), /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: "var(--font-mono)",
      fontSize: "var(--text-sm)",
      fontVariantNumeric: "tabular-nums",
      color: accent ? "var(--tallow-300)" : "var(--linen-200)"
    }
  }, value));
}

// Ambient overlay: cold corner shadow + faint air over the whole frame.
function Atmosphere() {
  return /*#__PURE__*/React.createElement("div", {
    "aria-hidden": "true",
    style: {
      position: "absolute",
      inset: 0,
      pointerEvents: "none",
      zIndex: 0,
      boxShadow: "inset 0 0 220px 50px rgba(4,6,6,.74)",
      background: "radial-gradient(140% 120% at 50% -10%, transparent 58%, rgba(4,6,6,.55))"
    }
  });
}
const frameStyle = {
  position: "relative",
  width: "100%",
  height: "100%",
  minHeight: 0,
  display: "flex",
  flexDirection: "column",
  overflow: "hidden",
  background: "radial-gradient(120% 100% at 50% 0%, #12181a, #060909 72%)"
};
const smallcaps = {
  margin: "0 0 10px",
  fontFamily: "var(--font-ui)",
  fontSize: "var(--text-xs)",
  fontWeight: 600,
  textTransform: "uppercase",
  letterSpacing: "var(--tracking-label)",
  color: "var(--text-body)"
};
window.GameScene = GameScene;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/clockwork-scene/GameScene.jsx", error: String((e && e.message) || e) }); }

// ui_kits/clockwork-world/App.jsx
try { (() => {
/* App — The Clockwork Dark: World & Interface.
   A grim-dark interactive bible: places, souls, things, the HUD, and
   the live playable scene. Ash & Thorn throughout. Sections are
   registered on window by their own files. */

const {
  useState: useAppState
} = React;
const TABS = [{
  id: "atlas",
  label: "Atlas",
  sub: "Places & buildings"
}, {
  id: "souls",
  label: "Souls",
  sub: "Characters, the cat, the wizard"
}, {
  id: "things",
  label: "Things",
  sub: "Items & relics"
}, {
  id: "interface",
  label: "Interface",
  sub: "HUD & panel design"
}, {
  id: "screens",
  label: "Screens",
  sub: "Trade · Bakery · Millhaven"
}, {
  id: "play",
  label: "Play",
  sub: "The live scene"
}];
function NavItem({
  tab,
  active,
  onClick
}) {
  return /*#__PURE__*/React.createElement("button", {
    onClick: onClick,
    style: {
      display: "block",
      width: "100%",
      textAlign: "left",
      cursor: "pointer",
      padding: "11px 16px",
      border: "none",
      borderLeft: "3px solid " + (active ? "var(--accent-candle)" : "transparent"),
      background: active ? "linear-gradient(90deg, rgba(214,178,108,.14), transparent)" : "transparent",
      transition: "all var(--dur-fast) var(--ease-quiet)"
    },
    onMouseEnter: e => {
      if (!active) e.currentTarget.style.background = "rgba(255,255,255,.03)";
    },
    onMouseLeave: e => {
      if (!active) e.currentTarget.style.background = "transparent";
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      display: "block",
      fontFamily: "var(--font-ui)",
      fontSize: "var(--text-base)",
      fontWeight: 600,
      letterSpacing: ".02em",
      color: active ? "var(--text-candlelight)" : "var(--text-on-dark)"
    }
  }, tab.label), /*#__PURE__*/React.createElement("span", {
    style: {
      display: "block",
      fontFamily: "var(--font-ui)",
      fontSize: "var(--text-xs)",
      color: "var(--text-muted)",
      marginTop: 2
    }
  }, tab.sub));
}
function App() {
  const [tab, setTab] = useAppState("atlas");
  const Section = {
    atlas: window.Atlas,
    souls: window.Souls,
    things: window.Things,
    interface: window.InterfaceKit,
    screens: window.Screens,
    play: window.PlaySection
  }[tab];
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: "grid",
      gridTemplateColumns: "248px 1fr",
      height: "100vh",
      minHeight: 0,
      background: "radial-gradient(120% 100% at 50% 0%, #10161a, #050807 72%)",
      color: "var(--text-on-dark)"
    }
  }, /*#__PURE__*/React.createElement("aside", {
    style: {
      display: "flex",
      flexDirection: "column",
      minHeight: 0,
      background: "linear-gradient(180deg,#090d0e,#060908)",
      borderRight: "1px solid rgba(214,178,108,.16)",
      boxShadow: "inset -20px 0 40px -30px #000"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      padding: "20px 16px 16px",
      borderBottom: "1px solid rgba(214,178,108,.12)"
    }
  }, /*#__PURE__*/React.createElement("img", {
    src: window.RES("../../assets/wordmark.svg"),
    alt: "The Clockwork Dark",
    style: {
      width: 196,
      filter: "drop-shadow(0 2px 10px rgba(0,0,0,.6))"
    }
  }), /*#__PURE__*/React.createElement("p", {
    style: {
      margin: "12px 2px 0",
      fontFamily: "var(--font-narration)",
      fontStyle: "italic",
      fontSize: "var(--text-sm)",
      color: "rgba(214,178,108,.6)"
    }
  }, "World & interface bible")), /*#__PURE__*/React.createElement("nav", {
    style: {
      padding: "10px 0",
      flex: 1,
      overflowY: "auto"
    }
  }, TABS.map(t => /*#__PURE__*/React.createElement(NavItem, {
    key: t.id,
    tab: t,
    active: tab === t.id,
    onClick: () => setTab(t.id)
  }))), /*#__PURE__*/React.createElement("div", {
    style: {
      padding: "14px 16px",
      borderTop: "1px solid rgba(214,178,108,.12)",
      fontFamily: "var(--font-mono)",
      fontSize: "10px",
      letterSpacing: ".06em",
      textTransform: "uppercase",
      color: "var(--text-muted)",
      lineHeight: 1.7
    }
  }, /*#__PURE__*/React.createElement("div", null, "Hearth Ledger \xB7 Ash & Thorn"), /*#__PURE__*/React.createElement("div", {
    style: {
      color: "rgba(214,178,108,.5)"
    }
  }, "v0.1 \xB7 grim-dark"))), /*#__PURE__*/React.createElement("main", {
    style: {
      minHeight: 0,
      overflowY: tab === "play" ? "hidden" : "auto",
      position: "relative"
    }
  }, Section ? /*#__PURE__*/React.createElement(Section, null) : /*#__PURE__*/React.createElement("div", {
    style: {
      padding: 40
    }
  }, "Loading\u2026")));
}
window.CWApp = App;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/clockwork-world/App.jsx", error: String((e && e.message) || e) }); }

// ui_kits/clockwork-world/Atlas.jsx
try { (() => {
/* Atlas — places & buildings of the Heartlands' margin. */

function PlaceCard({
  p
}) {
  return /*#__PURE__*/React.createElement("article", {
    style: {
      background: "linear-gradient(180deg,#0e1311,#0a0d0b)",
      border: "1px solid rgba(214,178,108,.14)",
      borderRadius: "var(--radius-sm)",
      overflow: "hidden",
      boxShadow: "0 14px 34px -16px rgba(0,0,0,.8)"
    }
  }, /*#__PURE__*/React.createElement(PaintFrame, {
    tint: p.tint,
    glow: p.glow,
    caption: p.caption,
    corrupted: p.corrupted,
    img: p.img,
    ratio: "16/9"
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      padding: "16px 18px 18px"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "baseline",
      justifyContent: "space-between",
      gap: 10
    }
  }, /*#__PURE__*/React.createElement("h3", {
    style: {
      margin: 0,
      fontFamily: "var(--font-narration)",
      fontSize: "var(--text-xl)",
      fontWeight: 500,
      color: "var(--text-on-dark)"
    }
  }, p.name), /*#__PURE__*/React.createElement(Pill, {
    brass: true
  }, p.kind)), /*#__PURE__*/React.createElement("p", {
    style: {
      margin: "9px 0 0",
      fontFamily: "var(--font-narration)",
      fontSize: "var(--text-base)",
      lineHeight: 1.5,
      color: "rgba(226,220,201,.7)"
    }
  }, p.blurb), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      flexWrap: "wrap",
      gap: 6,
      marginTop: 12
    }
  }, p.times.map(t => /*#__PURE__*/React.createElement(Pill, {
    key: t
  }, t))), /*#__PURE__*/React.createElement(Prompt, null, p.prompt), /*#__PURE__*/React.createElement("p", {
    style: {
      margin: "10px 0 0",
      fontFamily: "var(--font-ui)",
      fontSize: "var(--text-xs)",
      fontStyle: "italic",
      color: "var(--text-muted)"
    }
  }, p.note)));
}
function Atlas() {
  const places = window.CW_DATA.places;
  const weather = window.CW_DATA.weather;
  return /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement(SectionHead, {
    kicker: "The Atlas",
    title: "Places & buildings",
    lede: "A frontier village at the edge of an old forest. Beauty in bread steam and moss; dread at the margin where the wheat turns wrong. Every location is a ComfyUI 16:9 still \u2014 no characters centre-frame."
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      padding: "26px 40px 40px"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "grid",
      gridTemplateColumns: "repeat(auto-fill, minmax(360px, 1fr))",
      gap: 22
    }
  }, places.map(p => /*#__PURE__*/React.createElement(PlaceCard, {
    key: p.id,
    p: p
  }))), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 38
    }
  }, /*#__PURE__*/React.createElement(Kicker, null, "Weather \u2014 footer state & image modifier"), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      flexWrap: "wrap",
      gap: 12
    }
  }, weather.map(w => /*#__PURE__*/React.createElement("div", {
    key: w.key,
    style: {
      flex: "1 1 150px",
      minWidth: 150,
      padding: "14px 16px",
      borderRadius: "var(--radius-sm)",
      background: w.corrupted ? "rgba(122,158,79,.08)" : "rgba(255,255,255,.03)",
      border: "1px solid " + (w.corrupted ? "rgba(122,158,79,.3)" : "rgba(214,178,108,.16)")
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: "var(--font-mono)",
      fontSize: "var(--text-sm)",
      color: w.corrupted ? "var(--corruption)" : "var(--text-candlelight)",
      textTransform: "uppercase",
      letterSpacing: ".06em"
    }
  }, w.label), /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: "var(--font-ui)",
      fontSize: "var(--text-xs)",
      color: "var(--text-muted)",
      marginTop: 5
    }
  }, w.note)))))));
}
window.Atlas = Atlas;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/clockwork-world/Atlas.jsx", error: String((e && e.message) || e) }); }

// ui_kits/clockwork-world/Interface.jsx
try { (() => {
/* Interface — the HUD anatomy and panel designs. */

const IF = window.TheClockworkDarkDesignSystem_4a0a88;
function Card({
  title,
  children,
  span
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      gridColumn: span ? `span ${span}` : "auto",
      borderRadius: "var(--radius-md)",
      background: "linear-gradient(180deg,#0e1311,#090c0a)",
      border: "1px solid rgba(214,178,108,.14)",
      boxShadow: "0 14px 34px -18px rgba(0,0,0,.8)",
      overflow: "hidden"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      padding: "12px 16px",
      borderBottom: "1px solid rgba(214,178,108,.1)"
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: "var(--font-ui)",
      fontSize: "var(--text-xs)",
      fontWeight: 700,
      textTransform: "uppercase",
      letterSpacing: "var(--tracking-label)",
      color: "var(--accent-brass)"
    }
  }, title)), /*#__PURE__*/React.createElement("div", {
    style: {
      padding: 18
    }
  }, children));
}
function HudAnatomy() {
  const cell = (bg, label, sub, extra) => /*#__PURE__*/React.createElement("div", {
    style: {
      background: bg,
      border: "1px solid rgba(214,178,108,.16)",
      borderRadius: 3,
      padding: "10px 11px",
      display: "flex",
      flexDirection: "column",
      gap: 4,
      ...extra
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: "var(--font-ui)",
      fontSize: 10,
      fontWeight: 700,
      textTransform: "uppercase",
      letterSpacing: ".08em",
      color: "var(--text-candlelight)"
    }
  }, label), /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: "var(--font-ui)",
      fontSize: 10,
      color: "var(--text-muted)"
    }
  }, sub));
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: "grid",
      gridTemplateRows: "auto 1fr auto",
      gap: 6,
      height: 300
    }
  }, cell("linear-gradient(180deg,#0c0f0d,#0a0c0a)", "Header", "Scene name · World clock"), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "grid",
      gridTemplateColumns: "0.8fr 1.6fr 0.9fr",
      gap: 6,
      minHeight: 0
    }
  }, cell("linear-gradient(180deg,#141a16,#0d120f)", "Assistant", "200px · slides from left"), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "grid",
      gridTemplateRows: "1.1fr auto auto",
      gap: 6,
      minHeight: 0
    }
  }, cell("linear-gradient(160deg,#1a201b,#10140f)", "Scene visual", "ComfyUI still · 38vh"), cell("linear-gradient(180deg,#1c2019,#14160f)", "Narrative log", "SSE serif · the lit journal"), cell("#0d100d", "Choices + input", "2–4 chips · free text")), cell("linear-gradient(180deg,#181811,#11120b)", "Character sheet", "220px · HP · STA · inv")), cell("linear-gradient(0deg,#0c0f0d,#0a0c0a)", "Footer", "Day · time · weather · phase"));
}
function Letterbox() {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      position: "relative",
      aspectRatio: "2.39/1",
      background: "#000",
      borderRadius: 3,
      overflow: "hidden"
    }
  }, /*#__PURE__*/React.createElement("video", {
    src: window.RES('../../assets/video/cutscene-tower.mp4'),
    poster: window.RES('../../assets/art/scenes/clockwork-tower.jpg'),
    autoPlay: true,
    loop: true,
    muted: true,
    playsInline: true,
    style: {
      position: "absolute",
      inset: 0,
      width: "100%",
      height: "100%",
      objectFit: "cover"
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      inset: 0,
      backgroundImage: "var(--texture-paper)",
      opacity: .32,
      mixBlendMode: "multiply"
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      inset: 0,
      boxShadow: "inset 0 0 90px 20px rgba(6,8,5,.7)"
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      top: 0,
      left: 0,
      right: 0,
      height: 18,
      background: "#000"
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      left: 0,
      right: 0,
      bottom: 0,
      padding: "12px 16px",
      background: "linear-gradient(0deg, rgba(6,8,5,.92), transparent)"
    }
  }, /*#__PURE__*/React.createElement("p", {
    style: {
      margin: 0,
      fontFamily: "var(--font-narration)",
      fontStyle: "italic",
      fontSize: "var(--text-base)",
      color: "rgba(226,220,201,.92)",
      textShadow: "0 1px 3px #000"
    }
  }, "\"The village clock stopped at a hour that never was.\"")), /*#__PURE__*/React.createElement("button", {
    style: {
      position: "absolute",
      top: 10,
      right: 12,
      fontFamily: "var(--font-ui)",
      fontSize: 11,
      padding: "3px 9px",
      borderRadius: 3,
      cursor: "pointer",
      color: "rgba(226,220,201,.7)",
      background: "rgba(12,12,9,.5)",
      border: "1px solid rgba(214,178,108,.25)"
    }
  }, "Skip"));
}
const CUTSCENES = [{
  src: "../../assets/video/cutscene-misty-forest.mp4",
  poster: "../../assets/art/scenes/forest-mushroom-ring.jpg",
  cap: "Something watches from the stillness without moving."
}, {
  src: "../../assets/video/cutscene-golden-ring-bread.mp4",
  poster: "../../assets/art/things/golden-ring-in-bread.jpg",
  cap: "Bread that rings when it cracks."
}, {
  src: "../../assets/video/cutscene-wheatfield.mp4",
  poster: "../../assets/art/scenes/clockwork-wheatfield.jpg",
  cap: "Wheat rows tick like a metronome toward the horizon."
}, {
  src: "../../assets/video/cutscene-closing-gates.mp4",
  poster: "../../assets/art/scenes/closing-town-gates.jpg",
  cap: "Millhaven shuts the gate against the road."
}];
function CutsceneGallery() {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: "grid",
      gridTemplateColumns: "repeat(2, 1fr)",
      gap: 12
    }
  }, CUTSCENES.map(c => /*#__PURE__*/React.createElement("div", {
    key: c.src,
    style: {
      position: "relative",
      aspectRatio: "16/9",
      borderRadius: 3,
      overflow: "hidden",
      border: "1px solid rgba(214,178,108,.18)",
      background: "#000"
    }
  }, /*#__PURE__*/React.createElement("video", {
    src: window.RES(c.src),
    poster: window.RES(c.poster),
    autoPlay: true,
    loop: true,
    muted: true,
    playsInline: true,
    style: {
      position: "absolute",
      inset: 0,
      width: "100%",
      height: "100%",
      objectFit: "cover"
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      inset: 0,
      boxShadow: "inset 0 0 50px 8px rgba(6,8,5,.7)"
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      left: 0,
      right: 0,
      bottom: 0,
      padding: "9px 12px",
      background: "linear-gradient(0deg, rgba(6,8,5,.9), transparent)"
    }
  }, /*#__PURE__*/React.createElement("p", {
    style: {
      margin: 0,
      fontFamily: "var(--font-narration)",
      fontStyle: "italic",
      fontSize: "var(--text-sm)",
      color: "rgba(226,220,201,.92)",
      textShadow: "0 1px 3px #000"
    }
  }, c.cap)))));
}
function CombatSheet() {
  const {
    Button
  } = IF;
  return /*#__PURE__*/React.createElement("div", {
    style: {
      position: "relative",
      borderRadius: 3,
      overflow: "hidden",
      background: "linear-gradient(180deg,#15100f,#0c0a0a)",
      padding: 16,
      border: "1px solid rgba(122,45,42,.4)"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      inset: 0,
      backgroundImage: `url("${window.RES('../../assets/art/enemies/scarecrow-clockwork.jpg')}")`,
      backgroundSize: "cover",
      backgroundPosition: "center",
      opacity: .5
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      inset: 0,
      background: "linear-gradient(180deg, rgba(12,10,10,.5), rgba(12,10,10,.86))"
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      inset: 0,
      boxShadow: "inset 0 0 60px 8px rgba(107,45,45,.45)",
      pointerEvents: "none"
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: "relative"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      justifyContent: "space-between",
      alignItems: "baseline"
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: "var(--font-narration)",
      fontSize: "var(--text-lg)",
      color: "var(--text-on-dark)"
    }
  }, "Corrupted scarecrow"), /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: "var(--font-mono)",
      fontSize: "var(--text-sm)",
      color: "var(--status-danger)"
    }
  }, "HP 9")), /*#__PURE__*/React.createElement("div", {
    style: {
      height: 6,
      borderRadius: 3,
      marginTop: 8,
      background: "rgba(0,0,0,.5)",
      overflow: "hidden"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      width: "64%",
      height: "100%",
      background: "linear-gradient(90deg, var(--blood-quiet), #a14)"
    }
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      gap: 8,
      marginTop: 14,
      flexWrap: "wrap"
    }
  }, /*#__PURE__*/React.createElement(Button, {
    variant: "danger",
    size: "sm"
  }, "Strike"), /*#__PURE__*/React.createElement(Button, {
    variant: "secondary",
    size: "sm"
  }, "Ward"), /*#__PURE__*/React.createElement(Button, {
    variant: "secondary",
    size: "sm"
  }, "Flee")), /*#__PURE__*/React.createElement("p", {
    style: {
      margin: "12px 0 0",
      fontFamily: "var(--font-ui)",
      fontSize: 11,
      fontStyle: "italic",
      color: "var(--linen-300)"
    }
  }, "No battle animations in v0.1 \u2014 still image with a red vignette pulse.")));
}
function Interface() {
  const {
    AssistantBubble,
    DiceToast,
    ChoiceChip,
    WorldClock,
    Badge,
    StatLine
  } = IF;
  const phases = window.CW_DATA.phases;
  return /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement(SectionHead, {
    kicker: "The Interface",
    title: "HUD & panel design",
    lede: "A traveler's journal crossed with a clockmaker's ledger. No MMO clutter, no floating UI, no Awareness meter \u2014 hidden mechanics stay hidden until discovered in-world."
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      padding: "26px 40px 40px",
      display: "grid",
      gridTemplateColumns: "repeat(2, 1fr)",
      gap: 22
    }
  }, /*#__PURE__*/React.createElement(Card, {
    title: "HUD anatomy \u2014 global layout",
    span: 2
  }, /*#__PURE__*/React.createElement(HudAnatomy, null)), /*#__PURE__*/React.createElement(Card, {
    title: "Assistant bubble \u2014 forms & whisper"
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      flexDirection: "column",
      gap: 12
    }
  }, /*#__PURE__*/React.createElement(AssistantBubble, {
    form: "cat",
    style: {
      boxShadow: "var(--shadow-raise), 0 0 26px -6px rgba(214,178,108,.4)"
    }
  }, "The smoke is bread, not burning. Probably."), /*#__PURE__*/React.createElement(AssistantBubble, {
    form: "wanderer",
    whisper: true,
    style: {
      boxShadow: "var(--shadow-raise)"
    }
  }, "Roads change when the wheat turns wrong."))), /*#__PURE__*/React.createElement(Card, {
    title: "Dice toast \u2014 verbatim engine result"
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      flexDirection: "column",
      gap: 12,
      alignItems: "flex-start"
    }
  }, /*#__PURE__*/React.createElement(DiceToast, {
    roll: 14,
    modifier: 2,
    dc: 13,
    outcome: "Success"
  }), /*#__PURE__*/React.createElement(DiceToast, {
    roll: 4,
    modifier: 1,
    dc: 12,
    outcome: "Failure"
  }), /*#__PURE__*/React.createElement(DiceToast, {
    roll: 20,
    modifier: 0,
    outcome: "Boon"
  }))), /*#__PURE__*/React.createElement(Card, {
    title: "Choice chips \u2014 2\u20134, keyboard 1\u20134"
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      flexWrap: "wrap",
      gap: 8
    }
  }, /*#__PURE__*/React.createElement(ChoiceChip, {
    index: 1
  }, "Walk toward smoke"), /*#__PURE__*/React.createElement(ChoiceChip, {
    index: 2
  }, "Forage the clearing"), /*#__PURE__*/React.createElement(ChoiceChip, {
    index: 3
  }, "Listen"), /*#__PURE__*/React.createElement(ChoiceChip, {
    index: 4,
    disabled: true
  }, "Wait\u2026"))), /*#__PURE__*/React.createElement(Card, {
    title: "World clock & weather \u2014 diegetic"
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      flexDirection: "column",
      gap: 14
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      background: "var(--surface-chrome)",
      padding: "10px 14px",
      borderRadius: 3,
      display: "flex",
      justifyContent: "space-between"
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: "var(--font-ui)",
      fontSize: 12,
      textTransform: "uppercase",
      letterSpacing: ".1em",
      color: "var(--text-on-dark)"
    }
  }, "Edgewood Square"), /*#__PURE__*/React.createElement(WorldClock, {
    day: 12,
    time: "Evening",
    discovered: true
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      gap: 8,
      flexWrap: "wrap"
    }
  }, /*#__PURE__*/React.createElement(Badge, {
    tone: "neutral"
  }, "Overcast"), /*#__PURE__*/React.createElement(Badge, {
    tone: "candle"
  }, "Market day"), /*#__PURE__*/React.createElement(Badge, {
    tone: "corruption"
  }, "Wrong rain")))), /*#__PURE__*/React.createElement(Card, {
    title: "Character sheet \u2014 the ledger"
  }, /*#__PURE__*/React.createElement(StatLine, {
    label: "HP",
    value: "14/18"
  }), /*#__PURE__*/React.createElement(StatLine, {
    label: "Stamina",
    value: "6"
  }), /*#__PURE__*/React.createElement(StatLine, {
    label: "Gold",
    value: "0.42",
    accent: true
  }), /*#__PURE__*/React.createElement(StatLine, {
    label: "Location",
    value: "edgewood"
  })), /*#__PURE__*/React.createElement(Card, {
    title: "Cutscene \u2014 2.39:1 letterbox"
  }, /*#__PURE__*/React.createElement(Letterbox, null)), /*#__PURE__*/React.createElement(Card, {
    title: "Combat sheet \u2014 rare, minimal"
  }, /*#__PURE__*/React.createElement(CombatSheet, null)), /*#__PURE__*/React.createElement(Card, {
    title: "Cutscene gallery \u2014 6s AnimateDiff loops",
    span: 2
  }, /*#__PURE__*/React.createElement(CutsceneGallery, null)), /*#__PURE__*/React.createElement(Card, {
    title: "Phase transition \u2014 UI behavior",
    span: 2
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "grid",
      gridTemplateColumns: "repeat(4, 1fr)",
      gap: 14
    }
  }, phases.map((p, i) => /*#__PURE__*/React.createElement("div", {
    key: p.key,
    "data-phase": p.key,
    style: {
      borderRadius: 3,
      overflow: "hidden",
      border: "1px solid rgba(214,178,108,.16)"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      height: 52,
      background: "var(--surface-scene)",
      display: "grid",
      placeItems: "center",
      boxShadow: "inset 0 0 26px rgba(6,8,5,.7)"
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: "var(--font-mono)",
      fontSize: 11,
      color: "var(--accent-candle)"
    }
  }, "Day ", [4, 11, 22, 38][i])), /*#__PURE__*/React.createElement("div", {
    style: {
      padding: "10px 12px",
      background: "linear-gradient(180deg,#0e1311,#0a0d0b)"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: "var(--font-ui)",
      fontSize: 12,
      fontWeight: 700,
      textTransform: "uppercase",
      letterSpacing: ".06em",
      color: "var(--text-candlelight)"
    }
  }, p.label), /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: "var(--font-narration)",
      fontSize: 12,
      fontStyle: "italic",
      color: "rgba(226,220,201,.62)",
      marginTop: 4
    }
  }, p.mood), /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: "var(--font-ui)",
      fontSize: 11,
      color: "var(--text-muted)",
      marginTop: 6
    }
  }, p.ui))))))));
}
window.InterfaceKit = Interface;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/clockwork-world/Interface.jsx", error: String((e && e.message) || e) }); }

// ui_kits/clockwork-world/PaintFrame.jsx
try { (() => {
/* PaintFrame — a painterly placeholder frame standing in for ComfyUI art.
   Layered earth-gradient + candle bloom + paper grain + an abstract
   CSS silhouette. NOT final art: production stills are generated from
   the prompts shown beside each frame. Keeps everything honest while
   giving each subject a distinct, recognisable mood. */

const {
  useState: _useState
} = React;
function Silhouette({
  kind,
  robe = "#5a6a4a",
  accent = "#e8c47a",
  scale = 1
}) {
  const base = {
    position: "absolute",
    left: "50%",
    transform: "translateX(-50%)"
  };
  const eye = left => ({
    position: "absolute",
    top: 0,
    left,
    width: 6 * scale,
    height: 6 * scale,
    borderRadius: "50%",
    background: accent,
    boxShadow: `0 0 ${8 * scale}px ${accent}`
  });
  if (kind === "cat") {
    return /*#__PURE__*/React.createElement("div", {
      style: {
        position: "absolute",
        inset: 0
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        ...base,
        bottom: "8%",
        width: 120 * scale,
        height: 90 * scale,
        background: robe,
        borderRadius: "46% 46% 40% 40% / 60% 60% 40% 40%",
        filter: "blur(0.4px)"
      }
    }), /*#__PURE__*/React.createElement("div", {
      style: {
        ...base,
        bottom: "44%",
        marginLeft: -34 * scale,
        width: 0,
        height: 0,
        borderLeft: `${14 * scale}px solid transparent`,
        borderRight: `${10 * scale}px solid transparent`,
        borderBottom: `${26 * scale}px solid ${robe}`
      }
    }), /*#__PURE__*/React.createElement("div", {
      style: {
        ...base,
        bottom: "44%",
        marginLeft: 34 * scale,
        width: 0,
        height: 0,
        borderLeft: `${10 * scale}px solid transparent`,
        borderRight: `${14 * scale}px solid transparent`,
        borderBottom: `${26 * scale}px solid ${robe}`
      }
    }), /*#__PURE__*/React.createElement("div", {
      style: {
        ...base,
        bottom: "30%",
        width: 76 * scale,
        height: 64 * scale,
        background: robe,
        borderRadius: "48% 48% 46% 46%"
      }
    }), /*#__PURE__*/React.createElement("div", {
      style: {
        position: "absolute",
        bottom: "10%",
        right: "20%",
        width: 60 * scale,
        height: 16 * scale,
        background: robe,
        borderRadius: "50%",
        transform: "rotate(-28deg)"
      }
    }), /*#__PURE__*/React.createElement("div", {
      style: {
        ...base,
        bottom: "40%",
        width: 40 * scale,
        height: 6 * scale
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: eye(2)
    }), /*#__PURE__*/React.createElement("div", {
      style: eye(32 * scale)
    })));
  }
  if (kind === "hood" || kind === "wizard") {
    return /*#__PURE__*/React.createElement("div", {
      style: {
        position: "absolute",
        inset: 0
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        ...base,
        bottom: 0,
        width: 150 * scale,
        height: 170 * scale,
        background: `linear-gradient(180deg, ${robe} 0%, rgba(0,0,0,.55) 120%)`,
        borderRadius: "44% 44% 12% 12% / 70% 70% 12% 12%"
      }
    }), /*#__PURE__*/React.createElement("div", {
      style: {
        ...base,
        bottom: "44%",
        width: 104 * scale,
        height: 116 * scale,
        background: robe,
        borderRadius: "50% 50% 38% 38% / 62% 62% 40% 40%"
      }
    }), /*#__PURE__*/React.createElement("div", {
      style: {
        ...base,
        bottom: "52%",
        width: 52 * scale,
        height: 64 * scale,
        background: "radial-gradient(circle at 50% 40%, #0d100c, #14140f)",
        borderRadius: "50% 50% 46% 46%"
      }
    }), /*#__PURE__*/React.createElement("div", {
      style: {
        ...base,
        bottom: "64%",
        width: 34 * scale,
        height: 6 * scale
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: eye(0)
    }), /*#__PURE__*/React.createElement("div", {
      style: eye(28 * scale)
    })));
  }
  if (kind === "mirror") {
    return /*#__PURE__*/React.createElement("div", {
      style: {
        position: "absolute",
        inset: 0
      }
    }, /*#__PURE__*/React.createElement(Silhouette, {
      kind: "person",
      robe: robe,
      accent: accent,
      scale: scale * 0.82
    }), /*#__PURE__*/React.createElement("div", {
      style: {
        position: "absolute",
        inset: 0,
        top: "62%",
        transform: "scaleY(-1)",
        opacity: 0.4,
        maskImage: "linear-gradient(180deg, transparent, #000 80%)",
        WebkitMaskImage: "linear-gradient(180deg, transparent, #000 80%)"
      }
    }, /*#__PURE__*/React.createElement(Silhouette, {
      kind: "person",
      robe: accent,
      accent: robe,
      scale: scale * 0.82
    })));
  }
  if (kind === "mural") {
    // shrine wall: faceless saint arches + a brass gear hint
    const saint = left => /*#__PURE__*/React.createElement("div", {
      style: {
        position: "absolute",
        bottom: "10%",
        left,
        width: 40 * scale,
        height: 96 * scale,
        background: "linear-gradient(180deg, #2a2418, #14110b)",
        borderRadius: "50% 50% 8% 8% / 32% 32% 8% 8%",
        boxShadow: "inset 0 2px 6px rgba(232,196,122,.12)"
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        position: "absolute",
        top: 9 * scale,
        left: "50%",
        transform: "translateX(-50%)",
        width: 22 * scale,
        height: 22 * scale,
        borderRadius: "50%",
        background: "radial-gradient(circle at 50% 40%, #050604, #0d0b07)"
      }
    }));
    return /*#__PURE__*/React.createElement("div", {
      style: {
        position: "absolute",
        inset: 0
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        position: "absolute",
        inset: "8% 14% 0",
        background: "linear-gradient(180deg, #3a3020, #1c1710)",
        borderRadius: "40% 40% 0 0 / 14% 14% 0 0",
        boxShadow: "inset 0 0 40px rgba(0,0,0,.6)"
      }
    }), /*#__PURE__*/React.createElement("div", {
      style: {
        position: "absolute",
        left: "50%",
        bottom: 0,
        transform: "translateX(-50%)",
        display: "flex",
        gap: 12 * scale
      }
    }, saint(0), saint(0)), /*#__PURE__*/React.createElement("div", {
      style: {
        position: "absolute",
        top: "20%",
        left: "50%",
        transform: "translateX(-50%)",
        width: 30 * scale,
        height: 30 * scale,
        borderRadius: "50%",
        border: `${4 * scale}px solid ${accent}`,
        opacity: 0.7,
        boxShadow: `0 0 ${10 * scale}px ${accent}`,
        background: "transparent"
      }
    }));
  }
  if (kind === "barrow") {
    const stone = (left, h) => /*#__PURE__*/React.createElement("div", {
      style: {
        position: "absolute",
        bottom: "12%",
        left,
        width: 22 * scale,
        height: h * scale,
        background: "linear-gradient(180deg, #4a4e44, #1c211c)",
        borderRadius: "44% 44% 6% 6%",
        boxShadow: "inset 0 2px 6px rgba(255,255,255,.06)"
      }
    });
    return /*#__PURE__*/React.createElement("div", {
      style: {
        position: "absolute",
        inset: 0
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        position: "absolute",
        left: "50%",
        bottom: "6%",
        transform: "translateX(-50%)",
        width: 200 * scale,
        height: 90 * scale,
        background: "linear-gradient(180deg, #2e3a30, #141a14)",
        borderRadius: "50% 50% 12% 12% / 90% 90% 12% 12%"
      }
    }), /*#__PURE__*/React.createElement("div", {
      style: {
        position: "absolute",
        left: "50%",
        bottom: "8%",
        transform: "translateX(-50%)",
        width: 38 * scale,
        height: 56 * scale,
        background: "radial-gradient(120% 90% at 50% 100%, #000, #060906)",
        borderRadius: "50% 50% 0 0 / 70% 70% 0 0",
        boxShadow: `inset 0 6px 14px #000, 0 0 ${10 * scale}px ${hexShadow(accent)}`
      }
    }), stone("28%", 64), stone("66%", 54));
  }
  if (kind === "oven") {
    return /*#__PURE__*/React.createElement("div", {
      style: {
        position: "absolute",
        inset: 0
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        position: "absolute",
        left: "50%",
        bottom: "12%",
        transform: "translateX(-50%)",
        width: 150 * scale,
        height: 110 * scale,
        background: "linear-gradient(180deg, #4a4036, #1f1a14)",
        borderRadius: "50% 50% 14% 14% / 80% 80% 14% 14%",
        boxShadow: "inset 0 0 40px rgba(0,0,0,.5)"
      }
    }), /*#__PURE__*/React.createElement("div", {
      style: {
        position: "absolute",
        left: "50%",
        bottom: "16%",
        transform: "translateX(-50%)",
        width: 58 * scale,
        height: 40 * scale,
        background: `radial-gradient(120% 100% at 50% 100%, ${accent}, #7a3a10 60%, #1a0d06)`,
        borderRadius: "50% 50% 18% 18% / 64% 64% 18% 18%",
        boxShadow: `0 0 ${24 * scale}px ${accent}`
      }
    }));
  }

  // person / child
  const s = kind === "child" ? scale * 0.72 : scale;
  return /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      inset: 0
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      ...base,
      bottom: 0,
      width: 150 * s,
      height: 130 * s,
      background: `linear-gradient(180deg, ${robe} 0%, rgba(0,0,0,.5) 130%)`,
      borderRadius: "46% 46% 16% 16% / 64% 64% 16% 16%"
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      ...base,
      bottom: "46%",
      width: 72 * s,
      height: 86 * s,
      background: robe,
      borderRadius: "48% 48% 44% 44%"
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      ...base,
      bottom: "50%",
      width: 50 * s,
      height: 60 * s,
      background: "radial-gradient(circle at 50% 38%, rgba(0,0,0,.28), transparent 70%)",
      borderRadius: "50%"
    }
  }));
}
function PaintFrame({
  tint,
  glow,
  caption,
  sil,
  robe,
  accent,
  corrupted,
  ratio = "16/9",
  height,
  img,
  imgPos,
  children
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      position: "relative",
      width: "100%",
      aspectRatio: height ? undefined : ratio,
      height: height || undefined,
      overflow: "hidden",
      background: tint || "var(--surface-scene)",
      border: "var(--border-rule) solid var(--iron-900)",
      boxShadow: "var(--shadow-card)"
    }
  }, img && /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      inset: 0,
      backgroundImage: `url("${window.RES(img)}")`,
      backgroundSize: "cover",
      backgroundPosition: imgPos || "center",
      filter: corrupted ? "saturate(.82)" : "none"
    }
  }), glow && /*#__PURE__*/React.createElement("div", {
    className: "cw-flicker",
    style: {
      position: "absolute",
      inset: 0,
      background: glow,
      mixBlendMode: "screen",
      opacity: img ? 0.5 : 1
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      left: 0,
      right: 0,
      bottom: 0,
      height: "42%",
      background: "linear-gradient(0deg, rgba(160,150,120,.10), transparent)",
      mixBlendMode: "screen"
    }
  }), sil && !img && /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      left: "50%",
      bottom: "5%",
      width: "46%",
      height: 16,
      transform: "translateX(-50%)",
      borderRadius: "50%",
      background: "radial-gradient(closest-side, rgba(0,0,0,.55), transparent)",
      filter: "blur(2px)"
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      inset: 0,
      filter: `drop-shadow(0 0 1px ${accent || "#d6b26c"}) drop-shadow(0 0 9px ${hexShadow(accent)})`
    }
  }, /*#__PURE__*/React.createElement(Silhouette, {
    kind: sil,
    robe: robe,
    accent: accent
  }))), /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      top: "-10%",
      left: "30%",
      width: "40%",
      height: "85%",
      background: "linear-gradient(180deg, rgba(214,178,108,.12), transparent 72%)",
      transform: "skewX(-9deg)",
      mixBlendMode: "screen",
      pointerEvents: "none"
    }
  }), corrupted && /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      inset: 0,
      background: "var(--corruption)",
      opacity: 0.16,
      mixBlendMode: "color"
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      inset: 0,
      backgroundImage: "var(--texture-paper)",
      opacity: img ? 0.32 : 0.55,
      mixBlendMode: "multiply"
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      inset: 0,
      boxShadow: "inset 0 0 70px 12px rgba(8,9,6,.7)"
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      top: 0,
      left: 0,
      right: 0,
      height: 22,
      background: "linear-gradient(180deg, rgba(6,8,5,.6), transparent)"
    }
  }), /*#__PURE__*/React.createElement("span", {
    style: {
      position: "absolute",
      top: 8,
      right: 10,
      fontFamily: "var(--font-mono)",
      fontSize: 10,
      letterSpacing: ".08em",
      textTransform: "uppercase",
      color: "rgba(242,232,213,.5)"
    }
  }, "ComfyUI still"), caption && /*#__PURE__*/React.createElement("span", {
    style: {
      position: "absolute",
      left: 10,
      bottom: 10,
      fontFamily: "var(--font-narration)",
      fontStyle: "italic",
      fontSize: "var(--text-sm)",
      color: "rgba(242,232,213,.92)",
      textShadow: "0 1px 3px rgba(0,0,0,.6)"
    }
  }, caption), children);
}
window.Silhouette = Silhouette;
window.PaintFrame = PaintFrame;
function hexShadow(hex) {
  if (!hex || hex[0] !== "#") return "rgba(214,178,108,.35)";
  let h = hex.slice(1);
  if (h.length === 3) h = h.split("").map(c => c + c).join("");
  const n = parseInt(h, 16);
  return `rgba(${n >> 16 & 255}, ${n >> 8 & 255}, ${n & 255}, .35)`;
}
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/clockwork-world/PaintFrame.jsx", error: String((e && e.message) || e) }); }

// ui_kits/clockwork-world/Screens.jsx
try { (() => {
/* Screens — three full interface mockups: Trade, Bakery, Millhaven.
   Composes DS components in grim-dark Ash & Thorn. */

const SC = window.TheClockworkDarkDesignSystem_4a0a88;
const {
  useState: useScState,
  useEffect: useScEffect,
  useRef: useScRef
} = React;
function ScreenFrame({
  tint,
  caption,
  children,
  corrupted
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      borderRadius: "var(--radius-md)",
      overflow: "hidden",
      border: "1px solid rgba(214,178,108,.16)",
      boxShadow: "0 20px 50px -22px rgba(0,0,0,.85)",
      background: "linear-gradient(180deg,#0c100e,#080a09)"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      position: "relative",
      height: 150
    }
  }, /*#__PURE__*/React.createElement(PaintFrame, {
    tint: tint,
    caption: caption,
    corrupted: corrupted,
    height: 150
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      padding: 20
    }
  }, children));
}

/* ---------------- TRADE / BARTER OVERLAY ---------------- */
function TradeScreen() {
  const {
    Button,
    Badge
  } = SC;
  const give = [{
    name: "Wild mushroom",
    qty: 3,
    tint: "#8a6b4a",
    worth: 1
  }, {
    name: "Resin",
    qty: 2,
    tint: "#a9683a",
    worth: 1
  }, {
    name: "River clay",
    qty: 1,
    tint: "#7a6a52",
    worth: 1
  }];
  const get = [{
    name: "Sympathy charm",
    qty: 1,
    tint: "#b8863f",
    worth: 25,
    brass: true
  }, {
    name: "Tinker knowledge map",
    qty: 1,
    tint: "#caa05a",
    worth: 20
  }];
  const [offered, setOffered] = useScState([true, true, false]);
  const giveTotal = give.reduce((s, g, i) => s + (offered[i] ? g.worth * g.qty : 0), 0);
  const getTotal = 45;
  const balance = giveTotal - getTotal;
  const Row = ({
    it,
    on,
    toggle
  }) => /*#__PURE__*/React.createElement("button", {
    onClick: toggle,
    style: {
      display: "flex",
      alignItems: "center",
      gap: 12,
      width: "100%",
      textAlign: "left",
      cursor: toggle ? "pointer" : "default",
      padding: "9px 11px",
      borderRadius: "var(--radius-sm)",
      background: on === false ? "rgba(255,255,255,.02)" : "rgba(214,178,108,.07)",
      border: "1px solid " + (on === false ? "rgba(214,178,108,.1)" : "rgba(214,178,108,.22)"),
      marginBottom: 8
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      width: 30,
      height: 30,
      flex: "none",
      borderRadius: it.brass ? "50%" : 6,
      background: `linear-gradient(160deg, ${it.tint}, rgba(0,0,0,.55))`,
      border: it.brass ? "1px solid rgba(214,178,108,.5)" : "1px solid rgba(0,0,0,.4)",
      boxShadow: "inset 0 1px 2px rgba(255,255,255,.2)"
    }
  }), /*#__PURE__*/React.createElement("span", {
    style: {
      flex: 1,
      fontFamily: "var(--font-ui)",
      fontSize: "var(--text-base)",
      color: "var(--text-on-dark)"
    }
  }, it.name, " ", /*#__PURE__*/React.createElement("span", {
    style: {
      color: "var(--text-muted)",
      fontFamily: "var(--font-mono)",
      fontSize: 12
    }
  }, "\xD7", it.qty)), /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: "var(--font-mono)",
      fontSize: 12,
      color: "var(--text-candlelight)"
    }
  }, it.worth * it.qty, "c"));
  return /*#__PURE__*/React.createElement(ScreenFrame, {
    tint: "radial-gradient(110% 78% at 50% 18%, rgba(190,118,58,.30), transparent 52%), linear-gradient(178deg,#12120f 0%,#241a13 50%,#553a22 100%)",
    caption: "Ilya's wagon \xB7 barter, not coin"
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "baseline",
      justifyContent: "space-between",
      marginBottom: 16
    }
  }, /*#__PURE__*/React.createElement("h3", {
    style: {
      margin: 0,
      fontFamily: "var(--font-narration)",
      fontSize: "var(--text-xl)",
      color: "var(--text-on-dark)"
    }
  }, "Barter with Ilya of the Nine Pins"), /*#__PURE__*/React.createElement(Badge, {
    tone: "brass"
  }, "Caravan")), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "grid",
      gridTemplateColumns: "1fr 1fr",
      gap: 20
    }
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("p", {
    style: kickerS
  }, "You give"), give.map((g, i) => /*#__PURE__*/React.createElement(Row, {
    key: g.name,
    it: g,
    on: offered[i],
    toggle: () => setOffered(o => o.map((v, j) => j === i ? !v : v))
  })), /*#__PURE__*/React.createElement("p", {
    style: {
      fontFamily: "var(--font-ui)",
      fontSize: 11,
      color: "var(--text-muted)",
      fontStyle: "italic",
      margin: "4px 2px"
    }
  }, "Tap to add or hold back.")), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("p", {
    style: kickerS
  }, "Ilya offers"), get.map(g => /*#__PURE__*/React.createElement(Row, {
    key: g.name,
    it: g,
    on: true,
    toggle: null
  })))), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 18,
      padding: "14px 16px",
      borderRadius: "var(--radius-sm)",
      background: "rgba(0,0,0,.3)",
      border: "1px solid rgba(214,178,108,.16)"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      justifyContent: "space-between",
      alignItems: "center"
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: "var(--font-ui)",
      fontSize: 12,
      textTransform: "uppercase",
      letterSpacing: ".08em",
      color: "var(--text-muted)"
    }
  }, "Balance"), /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: "var(--font-mono)",
      fontSize: "var(--text-md)",
      color: balance >= 0 ? "#8fae5a" : "var(--status-danger)"
    }
  }, balance >= 0 ? "Fair — Ilya nods" : `${Math.abs(balance)}c short`)), /*#__PURE__*/React.createElement("div", {
    style: {
      height: 8,
      marginTop: 10,
      borderRadius: 4,
      background: "rgba(0,0,0,.5)",
      overflow: "hidden",
      position: "relative"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      left: "50%",
      top: 0,
      bottom: 0,
      width: 1,
      background: "rgba(214,178,108,.4)"
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      left: balance >= 0 ? "50%" : 50 + balance / getTotal * 50 + "%",
      right: balance >= 0 ? 50 - Math.min(balance, getTotal) / getTotal * 50 + "%" : "50%",
      top: 0,
      bottom: 0,
      background: balance >= 0 ? "linear-gradient(90deg,#5a6f3a,#8fae5a)" : "linear-gradient(90deg,#6b2d2d,#a14)"
    }
  }))), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      gap: 10,
      marginTop: 16,
      justifyContent: "flex-end"
    }
  }, /*#__PURE__*/React.createElement(Button, {
    variant: "ghost"
  }, "Step back"), /*#__PURE__*/React.createElement(Button, {
    variant: "primary",
    disabled: balance < 0
  }, "Strike the bargain")));
}

/* ---------------- BAKERY DOMESTIC UI ---------------- */
function OvenTimer() {
  const TOTAL = 12 * 60;
  const [left, setLeft] = useScState(7 * 60 + 42);
  const [running, setRunning] = useScState(true);
  useScEffect(() => {
    if (!running) return;
    const id = setInterval(() => setLeft(l => l <= 0 ? TOTAL : l - 1), 1000);
    return () => clearInterval(id);
  }, [running]);
  const pct = (1 - left / TOTAL) * 100;
  const mm = String(Math.floor(left / 60)).padStart(2, "0");
  const ss = String(left % 60).padStart(2, "0");
  const done = left <= 0;
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      gap: 12
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      position: "relative",
      width: 168,
      height: 168,
      borderRadius: "50%",
      background: `conic-gradient(var(--accent-candle) ${pct}%, rgba(255,255,255,.06) ${pct}%)`,
      display: "grid",
      placeItems: "center",
      boxShadow: "0 0 40px -8px rgba(214,178,108,.45)"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      inset: 12,
      borderRadius: "50%",
      background: "radial-gradient(circle at 50% 36%, #2a1c10, #120c07)",
      boxShadow: "inset 0 0 30px rgba(214,140,60,.4)",
      display: "grid",
      placeItems: "center"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      textAlign: "center"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: "var(--font-mono)",
      fontSize: 30,
      fontVariantNumeric: "tabular-nums",
      color: done ? "#8fae5a" : "var(--text-candlelight)"
    }
  }, done ? "Ready" : `${mm}:${ss}`), /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: "var(--font-ui)",
      fontSize: 10,
      textTransform: "uppercase",
      letterSpacing: ".14em",
      color: "var(--text-muted)",
      marginTop: 3
    }
  }, "Oven \xB7 loaf")))), /*#__PURE__*/React.createElement("button", {
    onClick: () => setRunning(r => !r),
    style: {
      fontFamily: "var(--font-ui)",
      fontSize: 12,
      padding: "5px 14px",
      borderRadius: "var(--radius-sm)",
      cursor: "pointer",
      color: "var(--text-candlelight)",
      background: "rgba(214,178,108,.1)",
      border: "1px solid rgba(214,178,108,.3)"
    }
  }, running ? "Tend the fire" : "Stoke"));
}
function BakeryScreen() {
  const {
    Button,
    Badge
  } = SC;
  const recipes = [{
    name: "Loaf of bread",
    needs: ["Flour", "Water", "Salt"],
    time: "12m",
    active: true
  }, {
    name: "Mushroom pottage",
    needs: ["Wild mushroom ×2", "Water", "Herbs"],
    time: "20m"
  }, {
    name: "Festival cake",
    needs: ["Flour", "Honey", "Dried fruit"],
    time: "35m"
  }];
  return /*#__PURE__*/React.createElement(ScreenFrame, {
    tint: "radial-gradient(90% 90% at 32% 56%, rgba(214,150,80,.46), transparent 60%), linear-gradient(178deg,#1a120c,#3a2414 60%,#6b4524 100%)",
    caption: "The Hearth Bakery \xB7 morning prep"
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "baseline",
      justifyContent: "space-between",
      marginBottom: 16
    }
  }, /*#__PURE__*/React.createElement("h3", {
    style: {
      margin: 0,
      fontFamily: "var(--font-narration)",
      fontSize: "var(--text-xl)",
      color: "var(--text-on-dark)"
    }
  }, "Maris's hearth \u2014 baking"), /*#__PURE__*/React.createElement(Badge, {
    tone: "candle"
  }, "Domestic")), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "grid",
      gridTemplateColumns: "200px 1fr",
      gap: 24,
      alignItems: "start"
    }
  }, /*#__PURE__*/React.createElement(OvenTimer, null), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("p", {
    style: kickerS
  }, "Recipes"), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      flexDirection: "column",
      gap: 10
    }
  }, recipes.map(r => /*#__PURE__*/React.createElement("div", {
    key: r.name,
    style: {
      padding: "11px 13px",
      borderRadius: "var(--radius-sm)",
      background: r.active ? "rgba(214,178,108,.08)" : "rgba(255,255,255,.02)",
      border: "1px solid " + (r.active ? "rgba(214,178,108,.28)" : "rgba(214,178,108,.1)")
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      justifyContent: "space-between",
      alignItems: "baseline"
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: "var(--font-narration)",
      fontSize: "var(--text-lg)",
      color: "var(--text-on-dark)"
    }
  }, r.name), /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: "var(--font-mono)",
      fontSize: 12,
      color: "var(--text-candlelight)"
    }
  }, r.time)), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      flexWrap: "wrap",
      gap: 6,
      marginTop: 8
    }
  }, r.needs.map(n => /*#__PURE__*/React.createElement("span", {
    key: n,
    style: {
      fontFamily: "var(--font-ui)",
      fontSize: 11,
      padding: "2px 8px",
      borderRadius: 999,
      background: "rgba(0,0,0,.3)",
      border: "1px solid rgba(214,178,108,.16)",
      color: "rgba(226,220,201,.72)"
    }
  }, n))), r.active && /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 11
    }
  }, /*#__PURE__*/React.createElement(Button, {
    variant: "primary",
    size: "sm"
  }, "Knead & set"))))), /*#__PURE__*/React.createElement("p", {
    style: {
      fontFamily: "var(--font-narration)",
      fontStyle: "italic",
      fontSize: "var(--text-base)",
      color: "rgba(214,178,108,.6)",
      margin: "16px 0 0"
    }
  }, "She hums to keep the gears quiet."))));
}

/* ---------------- MILLHAVEN MILITIA SCENE ---------------- */
function MillhavenScreen() {
  const {
    Button,
    ChoiceChip,
    Badge,
    StatLine,
    AssistantBubble
  } = SC;
  return /*#__PURE__*/React.createElement(ScreenFrame, {
    tint: "radial-gradient(120% 90% at 50% 16%, rgba(150,166,170,.20), transparent 55%), linear-gradient(178deg,#0c1114,#1d262b 55%,#39434a 100%)",
    caption: "Millhaven gate \xB7 cold rain"
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "baseline",
      justifyContent: "space-between",
      marginBottom: 14
    }
  }, /*#__PURE__*/React.createElement("h3", {
    style: {
      margin: 0,
      fontFamily: "var(--font-narration)",
      fontSize: "var(--text-xl)",
      color: "var(--text-on-dark)"
    }
  }, "The palisade gate"), /*#__PURE__*/React.createElement(Badge, {
    tone: "danger"
  }, "Duty")), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "grid",
      gridTemplateColumns: "1fr 220px",
      gap: 22
    }
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("p", {
    style: {
      fontFamily: "var(--font-narration)",
      fontSize: "var(--text-lg)",
      lineHeight: "var(--leading-relaxed)",
      color: "var(--text-narration)",
      margin: 0
    }
  }, "Sergeant Sera meets you under the dripping banner, scar pale in the lantern light. Refugees thin the mud road behind her. \"The road from the Heartlands is wrong tonight,\" she says. \"I can spare you the gate, or your silence. Not both.\""), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 16
    }
  }, /*#__PURE__*/React.createElement(AssistantBubble, {
    form: "wanderer",
    whisper: true,
    style: {
      boxShadow: "var(--shadow-raise)"
    }
  }, "She is not lying. That is what frightens her.")), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      flexWrap: "wrap",
      gap: 8,
      marginTop: 18
    }
  }, /*#__PURE__*/React.createElement(ChoiceChip, {
    index: 1
  }, "Show your road map"), /*#__PURE__*/React.createElement(ChoiceChip, {
    index: 2
  }, "Offer to stand the watch"), /*#__PURE__*/React.createElement(ChoiceChip, {
    index: 3
  }, "Ask what she saw"))), /*#__PURE__*/React.createElement("div", {
    style: {
      padding: "14px 15px",
      borderRadius: "var(--radius-sm)",
      background: "linear-gradient(180deg,#11161a,#0b0f12)",
      border: "1px solid rgba(150,166,170,.2)"
    }
  }, /*#__PURE__*/React.createElement("p", {
    style: {
      ...kickerS,
      color: "#9aa6a8"
    }
  }, "Gate watch"), /*#__PURE__*/React.createElement(StatLine, {
    label: "Militia",
    value: "6 fit"
  }), /*#__PURE__*/React.createElement(StatLine, {
    label: "Refugees",
    value: "23"
  }), /*#__PURE__*/React.createElement(StatLine, {
    label: "Rations",
    value: "4 days",
    accent: true
  }), /*#__PURE__*/React.createElement(StatLine, {
    label: "Road",
    value: "wrong"
  }), /*#__PURE__*/React.createElement("p", {
    style: {
      ...kickerS,
      color: "#9aa6a8",
      marginTop: 16
    }
  }, "Orders"), /*#__PURE__*/React.createElement("p", {
    style: {
      fontFamily: "var(--font-ui)",
      fontSize: 12,
      color: "rgba(226,220,201,.7)",
      lineHeight: 1.5,
      margin: 0
    }
  }, "Hold the gate. Admit the hungry. Report any brass."), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 14
    }
  }, /*#__PURE__*/React.createElement(Button, {
    variant: "danger",
    size: "sm",
    style: {
      width: "100%",
      justifyContent: "center"
    }
  }, "Sound the bell")))));
}
const kickerS = {
  margin: "0 0 12px",
  fontFamily: "var(--font-ui)",
  fontSize: "var(--text-xs)",
  fontWeight: 700,
  textTransform: "uppercase",
  letterSpacing: "var(--tracking-label)",
  color: "var(--accent-brass)"
};

/* ---------------- NOTICE BOARD / RUMORS ---------------- */
const PHASE_ORDER = ["dormant", "stirring", "spreading", "consuming"];
function NoticeBoardScreen() {
  const {
    Badge
  } = SC;
  const rumors = window.CW_DATA.rumors;
  const tones = {
    dormant: "neutral",
    stirring: "candle",
    spreading: "corruption",
    consuming: "danger"
  };
  const rot = [-1.4, 1.1, -0.8, 1.6, -1.2, 0.9, -1.6];
  return /*#__PURE__*/React.createElement(ScreenFrame, {
    tint: "radial-gradient(100% 80% at 50% 16%, rgba(150,120,70,.26), transparent 54%), linear-gradient(178deg,#13100b,#221a12 56%,#3a2c1c 100%)",
    caption: "Edgewood square \xB7 the notice board"
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "baseline",
      justifyContent: "space-between",
      marginBottom: 16
    }
  }, /*#__PURE__*/React.createElement("h3", {
    style: {
      margin: 0,
      fontFamily: "var(--font-narration)",
      fontSize: "var(--text-xl)",
      color: "var(--text-on-dark)"
    }
  }, "What the village is saying"), /*#__PURE__*/React.createElement(Badge, {
    tone: "brass"
  }, "Civic")), /*#__PURE__*/React.createElement("p", {
    style: {
      margin: "0 0 18px",
      fontFamily: "var(--font-narration)",
      fontSize: "var(--text-base)",
      fontStyle: "italic",
      color: "rgba(214,178,108,.7)"
    }
  }, "Fresh nails on the militia board \u2014 someone expects volunteers. The rumors arrive small and concrete; the dread is in the objects, never announced."), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "grid",
      gridTemplateColumns: "repeat(2, 1fr)",
      gap: 14
    }
  }, rumors.map((r, i) => /*#__PURE__*/React.createElement("div", {
    key: i,
    style: {
      position: "relative",
      padding: "16px 16px 14px",
      background: "linear-gradient(176deg, #e8ddc2, #d8cba8)",
      color: "#2a2418",
      borderRadius: 2,
      transform: `rotate(${rot[i % rot.length]}deg)`,
      boxShadow: "0 10px 22px -10px rgba(0,0,0,.75), inset 0 0 0 1px rgba(120,96,52,.25)"
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      position: "absolute",
      top: -6,
      left: "50%",
      transform: "translateX(-50%)",
      width: 13,
      height: 13,
      borderRadius: "50%",
      background: "radial-gradient(circle at 38% 32%, #f0d28a, #8a6a2e 70%, #5a4420)",
      boxShadow: "0 3px 6px rgba(0,0,0,.55)"
    }
  }), /*#__PURE__*/React.createElement("p", {
    style: {
      margin: 0,
      fontFamily: "var(--font-narration)",
      fontSize: "var(--text-base)",
      lineHeight: 1.5,
      color: "#2a2418"
    }
  }, r.text), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 11,
      display: "flex",
      justifyContent: "flex-end"
    }
  }, /*#__PURE__*/React.createElement(Badge, {
    tone: tones[r.phase]
  }, r.phase))))));
}

/* ---------------- SHRINE MURAL — interactive corruption reveal ---------------- */
function ShrineScreen() {
  const {
    Badge
  } = SC;
  const mural = window.CW_DATA.mural;
  const [reveal, setReveal] = useScState(1); // index into PHASE_ORDER
  const order = p => PHASE_ORDER.indexOf(p);
  return /*#__PURE__*/React.createElement(ScreenFrame, {
    tint: "radial-gradient(80% 78% at 50% 60%, rgba(214,178,108,.30), transparent 60%), linear-gradient(178deg,#160f0a,#2a1f14 56%,#42301c 100%)",
    caption: "Shrine of unnamed saints \xB7 the unfinished mural"
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "baseline",
      justifyContent: "space-between",
      marginBottom: 14
    }
  }, /*#__PURE__*/React.createElement("h3", {
    style: {
      margin: 0,
      fontFamily: "var(--font-narration)",
      fontSize: "var(--text-xl)",
      color: "var(--text-on-dark)"
    }
  }, "The wall nobody can finish"), /*#__PURE__*/React.createElement(Badge, {
    tone: "candle"
  }, "Sacred")), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "grid",
      gridTemplateColumns: "200px 1fr",
      gap: 22,
      alignItems: "start"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      borderRadius: "var(--radius-sm)",
      overflow: "hidden",
      border: "1px solid rgba(214,178,108,.2)"
    }
  }, /*#__PURE__*/React.createElement(PaintFrame, {
    tint: "linear-gradient(180deg,#2a2014,#140e08)",
    sil: "mural",
    accent: "#d6b26c",
    corrupted: order(PHASE_ORDER[reveal]) >= 2,
    height: 210,
    caption: null
  })), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("p", {
    style: kickerS
  }, "The mural gains a fragment as the dark deepens"), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      flexDirection: "column",
      gap: 9
    }
  }, mural.map((m, i) => {
    const lit = order(m.phase) <= reveal;
    return /*#__PURE__*/React.createElement("div", {
      key: i,
      style: {
        display: "flex",
        alignItems: "flex-start",
        gap: 11,
        padding: "9px 12px",
        borderRadius: "var(--radius-sm)",
        background: lit ? "rgba(214,178,108,.08)" : "rgba(255,255,255,.015)",
        border: "1px solid " + (lit ? "rgba(214,178,108,.24)" : "rgba(214,178,108,.08)"),
        opacity: lit ? 1 : 0.4,
        transition: "all var(--dur-base) var(--ease-quiet)"
      }
    }, /*#__PURE__*/React.createElement("span", {
      className: lit ? "cw-flicker" : "",
      style: {
        marginTop: 3,
        width: 7,
        height: 7,
        flex: "none",
        borderRadius: "50%",
        background: lit ? "var(--accent-candle)" : "#3a3a30",
        boxShadow: lit ? "0 0 10px var(--accent-candle)" : "none"
      }
    }), /*#__PURE__*/React.createElement("span", {
      style: {
        flex: 1,
        fontFamily: "var(--font-narration)",
        fontStyle: "italic",
        fontSize: "var(--text-base)",
        color: lit ? "rgba(226,220,201,.85)" : "var(--text-muted)"
      }
    }, lit ? m.frag : "— not yet painted —"), /*#__PURE__*/React.createElement("span", {
      style: {
        fontFamily: "var(--font-mono)",
        fontSize: 10,
        textTransform: "uppercase",
        letterSpacing: ".06em",
        color: "var(--text-muted)",
        marginTop: 4
      }
    }, m.phase));
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "center",
      gap: 8,
      marginTop: 16,
      flexWrap: "wrap"
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: "var(--font-ui)",
      fontSize: 11,
      textTransform: "uppercase",
      letterSpacing: ".08em",
      color: "var(--text-muted)"
    }
  }, "Reveal to"), PHASE_ORDER.map((p, i) => /*#__PURE__*/React.createElement("button", {
    key: p,
    onClick: () => setReveal(i),
    style: {
      fontFamily: "var(--font-ui)",
      fontSize: 11,
      textTransform: "capitalize",
      padding: "4px 11px",
      cursor: "pointer",
      borderRadius: "var(--radius-sm)",
      border: "1px solid " + (reveal === i ? "var(--accent-candle)" : "rgba(214,178,108,.2)"),
      background: reveal === i ? "rgba(214,178,108,.16)" : "transparent",
      color: reveal === i ? "var(--text-candlelight)" : "var(--text-muted)",
      boxShadow: reveal === i ? "0 0 14px -4px rgba(214,178,108,.6)" : "none"
    }
  }, p))), /*#__PURE__*/React.createElement("p", {
    style: {
      margin: "16px 0 0",
      fontFamily: "var(--font-narration)",
      fontStyle: "italic",
      fontSize: "var(--text-base)",
      color: "rgba(214,178,108,.6)"
    }
  }, "\"Finishing it would invite the road to arrive.\" \u2014 Greta Moss, shrine-keeper"))));
}
function Screens() {
  const [tab, setTab] = useScState("trade");
  const subs = [{
    id: "trade",
    label: "Trade · Barter"
  }, {
    id: "bakery",
    label: "Bakery · Hearth"
  }, {
    id: "millhaven",
    label: "Millhaven · Gate"
  }, {
    id: "board",
    label: "Notice · Board"
  }, {
    id: "shrine",
    label: "Shrine · Mural"
  }];
  const View = {
    trade: TradeScreen,
    bakery: BakeryScreen,
    millhaven: MillhavenScreen,
    board: NoticeBoardScreen,
    shrine: ShrineScreen
  }[tab];
  return /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement(SectionHead, {
    kicker: "The Screens",
    title: "Scenes & domestic UI",
    lede: "Beyond the forest turn: a barter overlay (goods, never floating coin), Maris's baking hearth, the cold militia gate, the village rumor board, and the shrine mural that paints the corruption one fragment at a time."
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      padding: "20px 40px 40px"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      flexWrap: "wrap",
      gap: 8,
      marginBottom: 22
    }
  }, subs.map(s => /*#__PURE__*/React.createElement("button", {
    key: s.id,
    onClick: () => setTab(s.id),
    style: {
      fontFamily: "var(--font-ui)",
      fontSize: "var(--text-sm)",
      fontWeight: 600,
      padding: "8px 16px",
      cursor: "pointer",
      borderRadius: "var(--radius-sm)",
      border: "1px solid " + (tab === s.id ? "var(--accent-candle)" : "rgba(214,178,108,.2)"),
      background: tab === s.id ? "rgba(214,178,108,.16)" : "transparent",
      color: tab === s.id ? "var(--text-candlelight)" : "var(--text-muted)",
      boxShadow: tab === s.id ? "0 0 16px -5px rgba(214,178,108,.55)" : "none",
      transition: "all var(--dur-fast) var(--ease-quiet)"
    }
  }, s.label))), /*#__PURE__*/React.createElement("div", {
    style: {
      maxWidth: 720
    }
  }, /*#__PURE__*/React.createElement(View, null))));
}
window.Screens = Screens;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/clockwork-world/Screens.jsx", error: String((e && e.message) || e) }); }

// ui_kits/clockwork-world/Souls.jsx
try { (() => {
/* Souls — the people, the cat, and the Assistant's many faces. */

function NpcCard({
  n
}) {
  return /*#__PURE__*/React.createElement("article", {
    style: {
      background: "linear-gradient(180deg,#0e1311,#0a0d0b)",
      border: "1px solid rgba(214,178,108,.14)",
      borderRadius: "var(--radius-sm)",
      overflow: "hidden",
      boxShadow: "0 14px 34px -16px rgba(0,0,0,.8)"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      position: "relative"
    }
  }, /*#__PURE__*/React.createElement(PaintFrame, {
    tint: n.tint,
    sil: n.sil,
    accent: n.accent,
    robe: "#2a2a22",
    img: n.img,
    ratio: "4/3",
    caption: n.role
  }), n.ambiguous && /*#__PURE__*/React.createElement("span", {
    style: {
      position: "absolute",
      top: 8,
      left: 10,
      fontFamily: "var(--font-mono)",
      fontSize: 9,
      letterSpacing: ".1em",
      textTransform: "uppercase",
      color: "rgba(214,178,108,.7)",
      background: "rgba(16,16,12,.6)",
      padding: "2px 6px",
      borderRadius: 3
    }
  }, "ambiguous")), /*#__PURE__*/React.createElement("div", {
    style: {
      padding: "14px 16px 16px"
    }
  }, /*#__PURE__*/React.createElement("h3", {
    style: {
      margin: 0,
      fontFamily: "var(--font-narration)",
      fontSize: "var(--text-lg)",
      fontWeight: 500,
      color: "var(--text-on-dark)"
    }
  }, n.name), /*#__PURE__*/React.createElement("p", {
    style: {
      margin: "3px 0 0",
      fontFamily: "var(--font-ui)",
      fontSize: "var(--text-xs)",
      textTransform: "uppercase",
      letterSpacing: ".06em",
      color: "var(--accent-brass)"
    }
  }, n.mood), /*#__PURE__*/React.createElement("p", {
    style: {
      margin: "9px 0 0",
      fontFamily: "var(--font-narration)",
      fontSize: "var(--text-base)",
      lineHeight: 1.5,
      color: "rgba(226,220,201,.7)"
    }
  }, n.blurb), /*#__PURE__*/React.createElement("p", {
    style: {
      margin: "10px 0 0",
      fontFamily: "var(--font-mono)",
      fontSize: "11px",
      color: "var(--text-muted)"
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      color: "var(--accent-brass)",
      textTransform: "uppercase",
      letterSpacing: ".08em"
    }
  }, "Voice"), " \xB7 ", n.voice)));
}
function RobePanel({
  r
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      borderRadius: "var(--radius-sm)",
      overflow: "hidden",
      border: "1px solid rgba(214,178,108,.16)",
      boxShadow: "0 14px 34px -16px rgba(0,0,0,.85)"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      position: "relative",
      height: 220,
      background: `radial-gradient(80% 60% at 50% 16%, rgba(214,178,108,.18), transparent 58%), linear-gradient(180deg, #0c0f0d, #07090800)`
    }
  }, /*#__PURE__*/React.createElement(PaintFrame, {
    tint: "linear-gradient(180deg,#0c100e,#070908)",
    sil: "wizard",
    robe: r.hex,
    accent: r.trim,
    height: 220
  }), /*#__PURE__*/React.createElement("span", {
    style: {
      position: "absolute",
      top: 9,
      left: 11,
      fontFamily: "var(--font-mono)",
      fontSize: 9,
      letterSpacing: ".1em",
      textTransform: "uppercase",
      color: "rgba(214,178,108,.7)",
      background: "rgba(12,12,9,.6)",
      padding: "2px 7px",
      borderRadius: 3
    }
  }, r.phase)), /*#__PURE__*/React.createElement("div", {
    style: {
      padding: "14px 16px 16px",
      background: "linear-gradient(180deg,#0e1311,#0a0d0b)"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "center",
      gap: 9
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      width: 16,
      height: 16,
      borderRadius: "50%",
      background: r.hex,
      boxShadow: "0 0 0 1px rgba(255,255,255,.12), 0 0 10px " + r.hex
    }
  }), /*#__PURE__*/React.createElement("h3", {
    style: {
      margin: 0,
      fontFamily: "var(--font-narration)",
      fontSize: "var(--text-lg)",
      fontWeight: 500,
      color: "var(--text-on-dark)"
    }
  }, r.name)), /*#__PURE__*/React.createElement("p", {
    style: {
      margin: "8px 0 0",
      fontFamily: "var(--font-ui)",
      fontSize: "var(--text-xs)",
      textTransform: "uppercase",
      letterSpacing: ".06em",
      color: "var(--accent-brass)"
    }
  }, r.reads), /*#__PURE__*/React.createElement("p", {
    style: {
      margin: "8px 0 0",
      fontFamily: "var(--font-narration)",
      fontSize: "var(--text-base)",
      lineHeight: 1.5,
      color: "rgba(226,220,201,.7)"
    }
  }, r.blurb)));
}
function FormChip({
  f
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      textAlign: "center"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      width: "100%",
      aspectRatio: "1/1",
      borderRadius: "var(--radius-sm)",
      overflow: "hidden",
      border: "1px solid rgba(214,178,108,.16)",
      position: "relative"
    }
  }, /*#__PURE__*/React.createElement(PaintFrame, {
    tint: "linear-gradient(180deg,#0e1311,#070908)",
    sil: f.sil,
    robe: f.robe,
    accent: "#d6b26c",
    img: f.img,
    height: 120
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 8,
      fontFamily: "var(--font-ui)",
      fontSize: "var(--text-sm)",
      fontWeight: 600,
      textTransform: "uppercase",
      letterSpacing: ".06em",
      color: "var(--text-candlelight)"
    }
  }, f.form), /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: "var(--font-ui)",
      fontSize: "11px",
      color: "var(--text-muted)",
      marginTop: 2
    }
  }, f.when), /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: "var(--font-narration)",
      fontStyle: "italic",
      fontSize: "12px",
      color: "rgba(226,220,201,.6)",
      marginTop: 4
    }
  }, f.note));
}
function Souls() {
  const D = window.CW_DATA;
  return /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement(SectionHead, {
    kicker: "The Souls",
    title: "Characters & the Assistant",
    lede: "Edgewood is poor but proud \u2014 frontier means mixed travelers, drawn with respect, never caricature. And the Assistant is never a tutorial fairy: it begins as a cat and grows into something robed and certain."
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      padding: "26px 40px 40px"
    }
  }, /*#__PURE__*/React.createElement(Kicker, null, "Villagers & the cat \u2014 portrait briefs (3:4)"), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "grid",
      gridTemplateColumns: "repeat(auto-fill, minmax(240px, 1fr))",
      gap: 20
    }
  }, D.npcs.map(n => /*#__PURE__*/React.createElement(NpcCard, {
    key: n.id,
    n: n
  }))), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 44,
      padding: "26px 28px",
      borderRadius: "var(--radius-md)",
      background: "radial-gradient(90% 100% at 50% 0%, rgba(190,118,58,.08), transparent 60%), linear-gradient(180deg,#0c100e,#080a09)",
      border: "1px solid rgba(214,178,108,.16)"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "baseline",
      justifyContent: "space-between",
      flexWrap: "wrap",
      gap: 10
    }
  }, /*#__PURE__*/React.createElement("h2", {
    style: {
      margin: 0,
      fontFamily: "var(--font-narration)",
      fontSize: "var(--text-2xl)",
      fontWeight: 500,
      color: "var(--text-on-dark)"
    }
  }, "The Assistant Wizard \u2014 robe study"), /*#__PURE__*/React.createElement("p", {
    style: {
      margin: 0,
      maxWidth: 420,
      fontFamily: "var(--font-narration)",
      fontStyle: "italic",
      fontSize: "var(--text-base)",
      color: "rgba(214,178,108,.7)"
    }
  }, "The hooded form's robe reads its intent. White mercy \u2192 grey watching \u2192 red appetite \u2192 black the Clockwork Dark itself.")), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "grid",
      gridTemplateColumns: "repeat(4, 1fr)",
      gap: 18,
      marginTop: 22
    }
  }, D.robes.map(r => /*#__PURE__*/React.createElement(RobePanel, {
    key: r.key,
    r: r
  })))), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 40
    }
  }, /*#__PURE__*/React.createElement(Kicker, null, "The five canonical forms"), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "grid",
      gridTemplateColumns: "repeat(5, 1fr)",
      gap: 16
    }
  }, D.assistantForms.map(f => /*#__PURE__*/React.createElement(FormChip, {
    key: f.form,
    f: f
  })))), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 40
    }
  }, /*#__PURE__*/React.createElement(Kicker, null, "Player archetypes \u2014 silhouette, not class"), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "grid",
      gridTemplateColumns: "repeat(3, 1fr)",
      gap: 18
    }
  }, D.archetypes.map(a => /*#__PURE__*/React.createElement("div", {
    key: a.id,
    style: {
      display: "flex",
      gap: 14,
      padding: "14px 16px",
      borderRadius: "var(--radius-sm)",
      background: "linear-gradient(180deg,#0e1311,#0a0d0b)",
      border: "1px solid rgba(214,178,108,.14)"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      width: 64,
      flex: "none",
      borderRadius: 3,
      overflow: "hidden",
      border: "1px solid rgba(214,178,108,.14)"
    }
  }, /*#__PURE__*/React.createElement(PaintFrame, {
    tint: a.tint,
    sil: "person",
    robe: "#2a2a20",
    accent: "#d6b26c",
    height: 84
  })), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("h3", {
    style: {
      margin: 0,
      fontFamily: "var(--font-narration)",
      fontSize: "var(--text-lg)",
      fontWeight: 500,
      color: "var(--text-on-dark)"
    }
  }, a.name), /*#__PURE__*/React.createElement("p", {
    style: {
      margin: "4px 0 0",
      fontFamily: "var(--font-ui)",
      fontSize: "var(--text-xs)",
      color: "var(--accent-brass)"
    }
  }, a.gear), /*#__PURE__*/React.createElement("p", {
    style: {
      margin: "5px 0 0",
      fontFamily: "var(--font-narration)",
      fontSize: "13px",
      color: "rgba(226,220,201,.65)"
    }
  }, a.look)))))), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 44
    }
  }, /*#__PURE__*/React.createElement(Kicker, null, "Bestiary \u2014 rare combat, no raid bosses"), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "grid",
      gridTemplateColumns: "repeat(auto-fill, minmax(240px, 1fr))",
      gap: 20
    }
  }, D.bestiary.map(b => /*#__PURE__*/React.createElement("article", {
    key: b.id,
    style: {
      background: "linear-gradient(180deg,#0e1311,#0a0d0b)",
      border: "1px solid " + (b.corrupted ? "rgba(122,158,79,.3)" : "rgba(214,178,108,.14)"),
      borderRadius: "var(--radius-sm)",
      overflow: "hidden",
      boxShadow: "0 14px 34px -16px rgba(0,0,0,.8)"
    }
  }, /*#__PURE__*/React.createElement(PaintFrame, {
    tint: "linear-gradient(180deg,#15100f,#0c0a0a)",
    img: b.img,
    corrupted: b.corrupted,
    ratio: "4/3",
    caption: b.when
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      padding: "14px 16px 16px"
    }
  }, /*#__PURE__*/React.createElement("h3", {
    style: {
      margin: 0,
      fontFamily: "var(--font-narration)",
      fontSize: "var(--text-lg)",
      fontWeight: 500,
      color: "var(--text-on-dark)"
    }
  }, b.name), /*#__PURE__*/React.createElement("p", {
    style: {
      margin: "3px 0 0",
      fontFamily: "var(--font-ui)",
      fontSize: "var(--text-xs)",
      textTransform: "uppercase",
      letterSpacing: ".06em",
      color: b.corrupted ? "var(--corruption)" : "var(--accent-brass)"
    }
  }, b.threat), /*#__PURE__*/React.createElement("p", {
    style: {
      margin: "9px 0 0",
      fontFamily: "var(--font-narration)",
      fontSize: "var(--text-base)",
      lineHeight: 1.5,
      color: "rgba(226,220,201,.7)"
    }
  }, b.blurb))))))));
}
window.Souls = Souls;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/clockwork-world/Souls.jsx", error: String((e && e.message) || e) }); }

// ui_kits/clockwork-world/Things.jsx
try { (() => {
/* Things — items, tools, wards, and the wrong relics. */

function ItemTile({
  it
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      borderRadius: "var(--radius-sm)",
      overflow: "hidden",
      border: "1px solid " + (it.corrupted ? "rgba(122,158,79,.3)" : "rgba(214,178,108,.14)"),
      background: "linear-gradient(180deg,#0e1311,#0a0d0b)",
      boxShadow: "0 10px 26px -14px rgba(0,0,0,.8)"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      position: "relative",
      height: 96,
      background: `radial-gradient(70% 80% at 50% 30%, ${hexA(it.tint, .9)}, ${hexA(it.tint, .25)} 70%, #0a0d0b)`,
      display: "grid",
      placeItems: "center"
    }
  }, it.img ?
  /*#__PURE__*/
  /* real oil-painted item icon */
  React.createElement("div", {
    style: {
      position: "absolute",
      inset: 0,
      backgroundImage: `url("${window.RES(it.img)}")`,
      backgroundSize: "cover",
      backgroundPosition: "center",
      filter: it.corrupted ? "saturate(.85)" : "none"
    }
  }) :
  /*#__PURE__*/
  /* item silhouette: a soft painterly lozenge tinted by the item */
  React.createElement("div", {
    style: {
      width: 46,
      height: 46,
      borderRadius: it.brass ? "50%" : "30% 30% 36% 36%",
      background: `linear-gradient(160deg, ${it.tint}, rgba(0,0,0,.5))`,
      boxShadow: "inset 0 1px 3px rgba(255,255,255,.2), 0 4px 10px rgba(0,0,0,.5)",
      border: it.brass ? "1px solid rgba(214,178,108,.5)" : "1px solid rgba(0,0,0,.3)"
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      inset: 0,
      backgroundImage: "var(--texture-paper)",
      opacity: it.img ? .26 : .4,
      mixBlendMode: "multiply"
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      inset: 0,
      boxShadow: "inset 0 0 30px rgba(8,9,6,.7)"
    }
  }), it.corrupted && /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      inset: 0,
      background: "var(--corruption)",
      opacity: .12,
      mixBlendMode: "color"
    }
  }), /*#__PURE__*/React.createElement("span", {
    style: {
      position: "absolute",
      top: 6,
      right: 7,
      fontFamily: "var(--font-mono)",
      fontSize: 9,
      color: it.corrupted ? "var(--corruption)" : "rgba(214,178,108,.6)",
      textTransform: "uppercase",
      letterSpacing: ".06em"
    }
  }, it.tag)), /*#__PURE__*/React.createElement("div", {
    style: {
      padding: "10px 12px 12px"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: "var(--font-ui)",
      fontSize: "var(--text-sm)",
      fontWeight: 600,
      color: "var(--text-on-dark)"
    }
  }, it.name), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      justifyContent: "space-between",
      alignItems: "baseline",
      marginTop: 5
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: "var(--font-ui)",
      fontSize: "11px",
      color: "var(--text-muted)"
    }
  }, it.from), /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: "var(--font-mono)",
      fontSize: "12px",
      color: it.price === "—" ? "var(--text-muted)" : "var(--text-candlelight)"
    }
  }, it.price))));
}
function hexA(hex, a) {
  const h = hex.replace("#", "");
  const n = parseInt(h.length === 3 ? h.split("").map(c => c + c).join("") : h, 16);
  return `rgba(${n >> 16 & 255}, ${n >> 8 & 255}, ${n & 255}, ${a})`;
}
function Things() {
  const items = window.CW_DATA.items;
  const groups = ["Food", "Forage", "Material", "Tool", "Arms", "Heal", "Knowledge", "Ward", "Light", "Apparel", "Craft", "Coin", "Quest", "Wrong"];
  const used = groups.filter(g => items.some(i => i.tag === g));
  return /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement(SectionHead, {
    kicker: "The Things",
    title: "Items & relics",
    lede: "Honest names, copper prices \u2014 never gold coins floating in the air. Item icons are flat 1:1 illustrations. The 'wrong' relics carry brass where brass should not be."
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      padding: "26px 40px 40px"
    }
  }, used.map(g => /*#__PURE__*/React.createElement("div", {
    key: g,
    style: {
      marginBottom: 30
    }
  }, /*#__PURE__*/React.createElement(Kicker, null, g === "Wrong" ? "Wrong — corruption relics (gated)" : g), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "grid",
      gridTemplateColumns: "repeat(auto-fill, minmax(168px, 1fr))",
      gap: 16
    }
  }, items.filter(i => i.tag === g).map(it => /*#__PURE__*/React.createElement(ItemTile, {
    key: it.name,
    it: it
  }))))), /*#__PURE__*/React.createElement("p", {
    style: {
      marginTop: 8,
      fontFamily: "var(--font-narration)",
      fontStyle: "italic",
      fontSize: "var(--text-base)",
      color: "rgba(214,178,108,.6)"
    }
  }, "Prices in copper \xB7 gold = 100 copper display. Seeds for each icon live in assets/comfyui-prompts.md.")));
}
window.Things = Things;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/clockwork-world/Things.jsx", error: String((e && e.message) || e) }); }

// ui_kits/clockwork-world/WorldKit.jsx
try { (() => {
/* Shared presentational helpers for the world bible — all grim-dark. */

function SectionHead({
  kicker,
  title,
  lede
}) {
  return /*#__PURE__*/React.createElement("header", {
    style: {
      padding: "34px 40px 18px",
      borderBottom: "1px solid rgba(214,178,108,.12)",
      position: "relative"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "center",
      gap: 10,
      marginBottom: 10
    }
  }, /*#__PURE__*/React.createElement("img", {
    src: window.RES("../../assets/gear-motif.svg"),
    alt: "",
    style: {
      width: 20,
      filter: "brightness(1.4) drop-shadow(0 0 10px rgba(190,118,58,.5))"
    }
  }), /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: "var(--font-ui)",
      fontSize: "var(--text-xs)",
      fontWeight: 700,
      textTransform: "uppercase",
      letterSpacing: "var(--tracking-title)",
      color: "var(--accent-brass)"
    }
  }, kicker)), /*#__PURE__*/React.createElement("h1", {
    style: {
      margin: 0,
      fontFamily: "var(--font-narration)",
      fontSize: "var(--text-3xl)",
      fontWeight: 500,
      color: "var(--text-on-dark)",
      letterSpacing: "-.01em",
      lineHeight: 1.05
    }
  }, title), lede && /*#__PURE__*/React.createElement("p", {
    style: {
      margin: "12px 0 0",
      maxWidth: 640,
      fontFamily: "var(--font-narration)",
      fontSize: "var(--text-lg)",
      lineHeight: var_relaxed,
      color: "rgba(226,220,201,.72)"
    }
  }, lede));
}
const var_relaxed = "var(--leading-relaxed)";
function Kicker({
  children
}) {
  return /*#__PURE__*/React.createElement("p", {
    style: {
      margin: "0 0 14px",
      fontFamily: "var(--font-ui)",
      fontSize: "var(--text-xs)",
      fontWeight: 700,
      textTransform: "uppercase",
      letterSpacing: "var(--tracking-label)",
      color: "var(--accent-brass)"
    }
  }, children);
}
function Prompt({
  children,
  neg
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 10,
      padding: "8px 11px",
      borderRadius: "var(--radius-sm)",
      background: "rgba(0,0,0,.32)",
      border: "1px solid rgba(214,178,108,.14)"
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      display: "block",
      fontFamily: "var(--font-mono)",
      fontSize: "10px",
      textTransform: "uppercase",
      letterSpacing: ".1em",
      color: "var(--accent-brass)",
      marginBottom: 3
    }
  }, neg ? "negative" : "ComfyUI prompt"), /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: "var(--font-mono)",
      fontSize: "11px",
      lineHeight: 1.5,
      color: "rgba(214,206,184,.78)"
    }
  }, children));
}
function Pill({
  children,
  brass
}) {
  return /*#__PURE__*/React.createElement("span", {
    style: {
      display: "inline-block",
      fontFamily: "var(--font-ui)",
      fontSize: "11px",
      padding: "2px 8px",
      borderRadius: "999px",
      letterSpacing: ".02em",
      color: brass ? "#14140f" : "rgba(226,220,201,.7)",
      background: brass ? "var(--accent-candle)" : "rgba(255,255,255,.05)",
      border: brass ? "none" : "1px solid rgba(214,178,108,.18)"
    }
  }, children);
}
Object.assign(window, {
  SectionHead,
  Kicker,
  Prompt,
  Pill
});
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/clockwork-world/WorldKit.jsx", error: String((e && e.message) || e) }); }

// ui_kits/clockwork-world/data.js
try { (() => {
/* The Clockwork Dark — world bible data.
   Drawn from data/lore/*.md, data/economy.yaml, data/procgen_templates/comfyui.yaml.
   Painterly placeholders are tuned per subject; production art is ComfyUI at runtime. */

window.CW_DATA = {
  // ---------------------------------------------------------------
  // PLACES & BUILDINGS  (location_still 16:9, 1344×768)
  // ---------------------------------------------------------------
  places: [{
    id: "forest_clearing",
    name: "The Forest Clearing",
    kind: "Wilds",
    tint: "linear-gradient(165deg,#324233 0%,#46553d 40%,#6d6a48 72%,#9a9258 100%)",
    glow: "radial-gradient(120% 80% at 50% 12%, rgba(232,196,122,.30), transparent 58%)",
    caption: "Birch margin · dawn mist",
    img: "../../assets/art/scenes/forest-mushroom-ring.jpg",
    blurb: "Where travelers wake. Birch and fern, mushroom circles, game trails that double back when watched. Smoke from Edgewood drifts west even when the wind blows south.",
    times: ["dawn mist", "noon", "blue hour"],
    prompt: "misty birch forest clearing, distant village smoke, mushrooms, ferns",
    note: "No minimap. Things watch from stillness without moving."
  }, {
    id: "edgewood_square",
    name: "Edgewood Square",
    kind: "Village",
    tint: "linear-gradient(165deg,#2c3a2a 0%,#4a4732 48%,#6e5a39 80%,#8a6b3f 100%)",
    glow: "radial-gradient(120% 80% at 62% 18%, rgba(232,196,122,.34), transparent 55%)",
    caption: "Communal oven · evening",
    img: "../../assets/art/scenes/town-scene.jpg",
    blurb: "Timber frames lean together around the communal stone oven. A shrine to unnamed saints never lacks a candle — though nobody can name the saints.",
    times: ["market day", "quiet evening"],
    prompt: "frontier village square, timber houses, communal stone oven, chickens",
    note: "NPC markers subtle — name on hover, never gamey icons."
  }, {
    id: "edgewood_bakery",
    name: "The Hearth Bakery",
    kind: "Interior",
    tint: "linear-gradient(165deg,#3a2a1f 0%,#6b4524 45%,#a9692f 76%,#e0a851 100%)",
    glow: "radial-gradient(90% 90% at 30% 60%, rgba(232,196,122,.46), transparent 60%)",
    caption: "Brick oven · morning prep",
    img: "../../assets/art/scenes/bakery.jpg",
    blurb: "Maris Hearth runs it with flour on her sleeves and a hum in her throat. Villagers say she hums to keep the gears quiet. Loaves that taste of honest hunger, not prophecy.",
    times: ["morning prep", "night, empty"],
    prompt: "small bakery interior, brick oven, flour sacks, warm light",
    note: "Domestic UI (recipes, oven timer) must look as polished as adventure UI."
  }, {
    id: "tinker_caravan",
    name: "The Tinker Caravan",
    kind: "Caravan",
    tint: "linear-gradient(165deg,#33281f 0%,#5a4128 46%,#8a5a2f 78%,#b8863f 100%)",
    glow: "radial-gradient(110% 80% at 50% 30%, rgba(201,122,60,.34), transparent 60%)",
    caption: "Nine-pin tent · arrival sunset",
    img: "../../assets/art/scenes/tinker-cart.jpg",
    blurb: "Ilya's wagon: tools, maps, hanging charms, chalk symbols, suspicious sympathy lamps. Maps of roads that shift when the wheat turns wrong.",
    times: ["arrival sunset", "rainy pack-up"],
    prompt: "colorful tinker tent, brass charms, maps, wagon wheels",
    note: "Trade UI is a barter list — not gold coins floating."
  }, {
    id: "millhaven_gate",
    name: "Millhaven Gate",
    kind: "Frontier",
    tint: "linear-gradient(165deg,#2a3036 0%,#43505a 46%,#5e6a6e 76%,#8a9088 100%)",
    glow: "radial-gradient(120% 90% at 50% 20%, rgba(180,190,190,.22), transparent 60%)",
    caption: "Palisade · cold rain",
    img: "../../assets/art/scenes/closing-town-gates.jpg",
    blurb: "A wooden palisade gate, militia banners, mud road, refugees. Sergeant Sera holds the line — duty-heavy, not a villain.",
    times: ["rain", "clear cold morning"],
    prompt: "wooden palisade gate, militia banners, mud road, refugees",
    note: "Rain variant; wrong_rain (falls upward) only STIRRING+."
  }, {
    id: "corruption_border",
    name: "The Corruption Border",
    kind: "Wrongness",
    tint: "linear-gradient(165deg,#222a1c 0%,#3c4a26 44%,#5e6b2c 74%,#8fae5a 100%)",
    glow: "radial-gradient(120% 90% at 50% 30%, rgba(143,174,90,.34), transparent 58%)",
    caption: "Brass in the wheat · SPREADING",
    img: "../../assets/art/scenes/clockwork-wheatfield.jpg",
    blurb: "A wheat field with brass gear growths, sick sky, wrong perspective. The wheat ticks like a metronome toward the horizon.",
    times: ["SPREADING phase only"],
    prompt: "wheat field with brass gear growths, sick sky, wrong perspective",
    corrupted: true,
    note: "Append corruption suffix: brass clockwork motifs in organic matter, sick green undertone."
  }, {
    id: "edgewood_shrine",
    name: "Shrine of Unnamed Saints",
    kind: "Sacred",
    tint: "linear-gradient(165deg,#241d18 0%,#3c3024 44%,#5a4630 74%,#7c5c38 100%)",
    glow: "radial-gradient(80% 70% at 50% 70%, rgba(232,196,122,.32), transparent 60%)",
    caption: "Candle wall · the unfinished mural",
    blurb: "A shrine to saints nobody can name never lacks a candle. Its wall bears an incomplete mural \u2014 saints with missing faces, wheat threaded with brass, a road winding inward. Old women say finishing it would invite the road to arrive.",
    times: ["votive dusk", "empty noon"],
    prompt: "village shrine wall, incomplete mural, votive candles, faceless saints, brass-threaded wheat",
    note: "The mural gains a fragment each phase \u2014 corruption told through the wall, not the HUD."
  }, {
    id: "hollow_hill",
    name: "Hollow Hill",
    kind: "Barrow",
    tint: "linear-gradient(165deg,#1c2420 0%,#2e3a30 46%,#46503e 76%,#5e6347 100%)",
    glow: "radial-gradient(110% 80% at 50% 86%, rgba(122,158,79,.16), transparent 60%)",
    caption: "Standing stones \u00b7 a door best left shut",
    img: "../../assets/art/scenes/forest-hidden-tunnel.jpg",
    blurb: "A hidden path off the game trails leads to barrows older than the village. Turf-roofed stone, a lintel worn smooth, dark beneath. Best left unopened until nerve and need align \u2014 the First Warden sleeps here, and not alone.",
    times: ["grey morning", "moonless"],
    prompt: "ancient turf-covered barrow mound, standing stones, dark stone doorway, mist",
    note: "Reachable only via a discovered hidden_path. Wrong-green seeps from the door at SPREADING+."
  }, {
    id: "marches_road",
    name: "The Marches Road",
    kind: "Wrongness",
    tint: "linear-gradient(165deg,#20271c 0%,#37431f 44%,#5c6a2c 74%,#94b25c 100%)",
    glow: "radial-gradient(120% 90% at 50% 18%, rgba(143,174,90,.30), transparent 56%)",
    caption: "The road winding inward \u00b7 SPREADING",
    img: "../../assets/art/scenes/wheatfield-forest-edge.jpg",
    blurb: "The track that leaves Edgewood for the Heartlands. It took Odran an extra hour though the sun said otherwise. Milestones count down to a number that is not a distance. Walk it long enough and the wheat begins to stand in rows too straight for wind.",
    times: ["SPREADING phase only"],
    prompt: "frontier road winding toward distant wound of light, straight wheat rows, sick sky, wrong perspective",
    corrupted: true,
    note: "Milestones tick instead of measuring. The road is longer leaving than returning."
  }, {
    id: "resting_camp",
    name: "The Roadside Camp",
    kind: "Wilds",
    tint: "linear-gradient(165deg,#231d16 0%,#39301f 44%,#5a4628 74%,#7c5e34 100%)",
    glow: "radial-gradient(70% 60% at 42% 64%, rgba(232,170,90,.36), transparent 60%)",
    caption: "Banked fire \u00b7 a night between roads",
    img: "../../assets/art/scenes/resting-camp.jpg",
    blurb: "A bedroll, a banked fire, a kettle going cold. Travelers rest here between the clearing and the gate \u2014 no inn, no walls, only the fire and whatever the dark brings to its edge. Stamina returns; nerve does not, always.",
    times: ["first watch", "grey dawn"],
    prompt: "roadside travelers' camp at night, bedroll, banked campfire, kettle, dark treeline",
    note: "Rest scene \u2014 stamina recovers. Encounters may interrupt at STIRRING+."
  }, {
    id: "ruins_temple",
    name: "The Mage-Ruins",
    kind: "Ruins",
    tint: "linear-gradient(165deg,#1d2128 0%,#2f3640 46%,#4a4c4a 76%,#6a6356 100%)",
    glow: "radial-gradient(100% 78% at 50% 40%, rgba(190,118,58,.20), transparent 58%)",
    caption: "Broken colonnade \u00b7 older than the wound",
    img: "../../assets/art/scenes/ruins-temple-mages.jpg",
    blurb: "Toppled columns and a temple floor swallowed by root and moss. Whoever raised it knew the Clockwork Dark by an older name. Robed figures are carved into the stone \u2014 or were, once, standing where you stand now.",
    times: ["overcast", "storm-light"],
    prompt: "ruined temple colonnade, mossy broken columns, robed figures, grey storm light",
    note: "Lore-gate location. The carvings answer to ward pins."
  }, {
    id: "clockwork_tower",
    name: "The Clockwork Tower",
    kind: "Wrongness",
    tint: "linear-gradient(165deg,#181b14 0%,#2c3318 46%,#4a5220 74%,#7c8a3a 100%)",
    glow: "radial-gradient(90% 80% at 50% 24%, rgba(143,174,90,.30), transparent 56%)",
    caption: "The heart of the wound \u00b7 CONSUMING",
    img: "../../assets/art/scenes/clockwork-tower.jpg",
    blurb: "Where the road has been counting toward. A spire of meshed brass and blackened stone rising from a field that ticks. The Clockwork Dark is not a demon you can banish \u2014 it is a logic, and this is where the logic keeps its time.",
    times: ["CONSUMING phase only"],
    prompt: "vast clockwork tower of brass gears and black stone, ticking wheat plain, bruised sky",
    corrupted: true,
    note: "End-state location. Visible on the horizon from SPREADING; reachable only at CONSUMING."
  }],
  // ---------------------------------------------------------------
  // SOULS  (portrait 3:4, 768×1024)
  // ---------------------------------------------------------------
  npcs: [{
    id: "npc_maris",
    name: "Maris Hearth",
    role: "The Baker",
    tint: "linear-gradient(160deg,#3a2a1f 0%,#7a4f2a 55%,#d2a256 100%)",
    sil: "person",
    accent: "#e8c47a",
    mood: "Warmth with worry underneath",
    blurb: "Woman, 40s, flour on her forearms, kind tired eyes. She hums to keep the gears quiet and buys wild mushrooms from travelers.",
    prompt: "woman, 40s, flour on forearms, kind eyes, tired, bakery interior, oven glow",
    voice: "Soft maternal · flour in the voice"
  }, {
    id: "npc_odran",
    name: "Odran Cartwright",
    role: "Caravan Master",
    tint: "linear-gradient(160deg,#2f2922 0%,#6b5236 55%,#b8863f 100%)",
    sil: "person",
    accent: "#c97a3c",
    mood: "Merchant cheer masking gossip hunger",
    blurb: "Man, 50s, weathered, a ledger always in hand, horse whip coiled at his belt. He trades twice a season and remembers every debt.",
    prompt: "man, 50s, weathered, ledger in hand, horse whip coiled, wagon trail at dusk",
    voice: "Merchant boom · brisk"
  }, {
    id: "npc_ilya",
    name: "Ilya of the Nine Pins",
    role: "The Tinker",
    img: "../../assets/art/souls/tinker.jpg",
    tint: "linear-gradient(160deg,#33281f 0%,#7a5530 55%,#caa05a 100%)",
    sil: "person",
    accent: "#b8863f",
    mood: "Curious · a slightly unsettling smile",
    blurb: "Androgynous, sharp eyes, nine brass pins in the scarf. Sells sympathy charms and ward pins that sometimes work and sometimes merely reassure.",
    prompt: "androgynous, sharp eyes, nine brass pins in scarf, tent interior, hanging charms",
    voice: "Precise · careful",
    ambiguous: true
  }, {
    id: "npc_sera",
    name: "Sergeant Sera Venn",
    role: "Militia",
    tint: "linear-gradient(160deg,#2a3036 0%,#4a565c 55%,#8a9088 100%)",
    sil: "person",
    accent: "#9aa0a0",
    mood: "Duty-heavy · not a villain",
    blurb: "Woman, 30s, a scar on her cheek, practical armor. She holds Millhaven gate in the rain while refugees thin the road behind her.",
    prompt: "woman, 30s, scar on cheek, practical armor, Millhaven gate, rain",
    voice: "Level · weary command"
  }, {
    id: "npc_brindle",
    name: "Brindle",
    role: "Barn Cat · Assistant form",
    img: "../../assets/art/souls/cat-assistant.jpg",
    tint: "linear-gradient(160deg,#2c3a2a 0%,#4a4732 55%,#6e6a45 100%)",
    sil: "cat",
    accent: "#e8c47a",
    mood: "Cute, but uncanny",
    blurb: "A grey barn cat with too-knowing eyes and a curled tail. Sits at the village square's edge. The Assistant's earliest, lowest-trust face.",
    prompt: "grey barn cat, too-knowing eyes, tail curled, village square edge",
    voice: "— optional chime instead of voice",
    ambiguous: true
  }, {
    id: "npc_greta",
    name: "Greta Moss",
    role: "The Shrine-keeper",
    tint: "linear-gradient(160deg,#2a241c 0%,#5a4a34 55%,#9a824e 100%)",
    sil: "person",
    accent: "#cbb07a",
    mood: "Piety thinned to warning",
    blurb: "Woman, 70s, votive wax on her knuckles and a saint's-bell at her belt. She tends the candles and refuses to finish the mural. She knew the road would change before the traders did, and she will not say how.",
    prompt: "old woman, 70s, votive wax on knuckles, shawl, shrine candlelight, faceless mural behind",
    voice: "Dry · scripture worn to plain warning"
  }, {
    id: "npc_wren",
    name: "Wren",
    role: "The Gear-child",
    img: "../../assets/art/souls/child-assistant.jpg",
    tint: "linear-gradient(160deg,#26302a 0%,#46503c 55%,#6e6a48 100%)",
    sil: "child",
    accent: "#e8c47a",
    mood: "Draws what is coming",
    blurb: "A village child, maybe nine, charcoal on the fingers. Draws interlocking gears in the dirt of the square; by morning the drawings are gone. Says a quiet friend showed her how. Overlaps the Assistant's child form \u2014 nobody is certain which is which.",
    prompt: "child, 9, charcoal-stained fingers, drawing gears in dirt, village square dusk",
    voice: "Small · matter-of-fact about impossible things",
    ambiguous: true
  }, {
    id: "npc_aldric",
    name: "Aldric Thorn",
    role: "The Woodcutter",
    tint: "linear-gradient(160deg,#222a20 0%,#3e4a32 55%,#6a6e48 100%)",
    sil: "person",
    accent: "#9aa06a",
    mood: "Practical · spooked by his own woods",
    blurb: "Man, 40s, axe over one shoulder, sawdust in his beard. He cuts the margin timber and knows which trails double back. Lately he will not work past the third birch \u2014 the game trails, he says, have started watching him back.",
    prompt: "woodcutter, 40s, axe on shoulder, sawdust beard, forest margin, long shadows",
    voice: "Blunt · fewer words after dark"
  }],
  // Player archetypes — silhouette, not class
  archetypes: [{
    id: "wayfarer",
    name: "Wayfarer",
    gear: "Cloak, staff, road boots",
    look: "Travel-worn, practical",
    tint: "linear-gradient(160deg,#2c3a2a,#5a6a4a)"
  }, {
    id: "hearthkeeper",
    name: "Hearthkeeper",
    gear: "Apron, rolled sleeves",
    look: "Flour dust, warm colors",
    tint: "linear-gradient(160deg,#5a3a22,#c79a4a)"
  }, {
    id: "tinker",
    name: "Tinker-apprentice",
    gear: "Tool belt, goggles",
    look: "Brass pins, chalk stains",
    tint: "linear-gradient(160deg,#3a2f24,#a9683a)"
  }],
  // ---------------------------------------------------------------
  // BESTIARY — rare, minimal combat. No raid bosses, no glow.
  // ---------------------------------------------------------------
  bestiary: [{
    id: "wolf",
    name: "Forest wolf",
    threat: "Hungry, not evil",
    when: "Any phase · birch dusk",
    img: "../../assets/art/enemies/wolf.jpg",
    blurb: "Lean and rain-wet, ribs showing. The honest danger of the margin — it wants the meat in your pack, not your soul. Flee is a real option."
  }, {
    id: "deserter",
    name: "Militia deserter",
    threat: "Desperate human",
    when: "STIRRING · the wet road",
    img: "../../assets/art/souls/warrior.jpg",
    blurb: "A man who left Millhaven's gate before it shut. Mud, a notched blade, eyes that already lost. He is not a monster — which is the worst of it."
  }, {
    id: "scarecrow",
    name: "Field scarecrow",
    threat: "Wrong, standing too still",
    when: "STIRRING · wheat margin",
    img: "../../assets/art/enemies/scarecrow.jpg",
    blurb: "It was a scarecrow yesterday. Today it faces the road, and nobody turned it. The first thing the wheat-corruption wears."
  }, {
    id: "scarecrow_brass",
    name: "Corrupted scarecrow",
    threat: "Brass nails, wrong shadow",
    when: "SPREADING",
    img: "../../assets/art/enemies/scarecrow-clockwork.jpg",
    blurb: "Brass driven where straw should be, a shadow that falls the wrong way. It ticks. When it moves you wish it had stayed a scarecrow.",
    corrupted: true
  }, {
    id: "clockwork_beast",
    name: "Clockwork beast",
    threat: "Gears in muscle",
    when: "SPREADING · the border",
    img: "../../assets/art/enemies/clockwork-monster-vs-mage.jpg",
    blurb: "Something that was an animal, rebuilt by the logic into a thing of meshed brass and meat. It does not hunger. It only continues.",
    corrupted: true
  }, {
    id: "husk",
    name: "Clockwork husk",
    threat: "A clock where the heart was",
    when: "CONSUMING only",
    img: "../../assets/art/souls/clockwork-mage.jpg",
    blurb: "Brass ribs, linen tear, a stopped watch where the heart should beat. Not a raid boss — a person the Clockwork Dark finished with. It keeps the wrong hour.",
    corrupted: true
  }],
  // ---------------------------------------------------------------
  // THE ASSISTANT — five canonical forms + the robed wizard study
  // ---------------------------------------------------------------
  assistantForms: [{
    form: "cat",
    when: "Early game · low trust",
    note: "Brindle, or a strange stray",
    sil: "cat",
    robe: "#5a6a4a",
    img: "../../assets/art/souls/cat-assistant.jpg"
  }, {
    form: "wanderer",
    when: "Whisper arc",
    note: "Grey cloak, face in shadow",
    sil: "hood",
    robe: "#6a6e6a",
    img: "../../assets/art/souls/assistant-mage.jpg"
  }, {
    form: "child",
    when: "STIRRING anomalies",
    note: "Draws gears in the dirt",
    sil: "child",
    robe: "#8a7a5a",
    img: "../../assets/art/souls/child-assistant.jpg"
  }, {
    form: "tinker",
    when: "Trade / knowledge",
    note: "Overlaps Ilya — ambiguous",
    sil: "hood",
    robe: "#a9683a",
    img: "../../assets/art/souls/tinker.jpg"
  }, {
    form: "reflection",
    when: "High Awareness",
    note: "Player silhouette in water",
    sil: "mirror",
    robe: "#4a565c",
    img: "../../assets/art/souls/shadow-mage-assistant.jpg"
  }],
  // The robed wizard assistant — color study. The Assistant grows from
  // a cat into a hooded figure; the robe color reads its intent.
  robes: [{
    key: "white",
    name: "White Robe",
    hex: "#e9e2cd",
    trim: "#c7b98e",
    ink: "#3a3326",
    reads: "Mercy / the guide it pretends to be",
    phase: "DORMANT",
    blurb: "Linen-pale, almost saintly. The Assistant at its most reassuring — and least trustworthy. Bright until the line lands wrong."
  }, {
    key: "grey",
    name: "Grey Robe",
    hex: "#6a6e6a",
    trim: "#4a4e4a",
    ink: "#e9e2cd",
    reads: "The wanderer · neutral, watching",
    phase: "STIRRING",
    blurb: "Road-dust grey, face in shadow. The whisper-arc form: dry, tired, pausing mid-sentence. It knows the road changed before you did."
  }, {
    key: "red",
    name: "Red Robe",
    hex: "#7a2f2a",
    trim: "#5a201d",
    ink: "#f2e8d5",
    reads: "Appetite / the gears beneath",
    phase: "SPREADING",
    blurb: "Quiet blood, not heraldry. Worn when the Assistant's interest sharpens into hunger. Brass threads catch the firelight at the hem."
  }, {
    key: "black",
    name: "Black Robe",
    hex: "#1b1b18",
    trim: "#3a3a30",
    ink: "#d9b25f",
    reads: "The Clockwork Dark itself",
    phase: "CONSUMING",
    blurb: "Ironwood black, clockwork filigree at the cuffs. The form it wears when ambiguity is over. Candlelight makes the gears move."
  }],
  // ---------------------------------------------------------------
  // THINGS  (item_icon 1:1, 256×256, flat illustrative)
  // ---------------------------------------------------------------
  items: [{
    name: "Loaf of bread",
    tag: "Food",
    price: "2c",
    from: "Maris",
    tint: "#c79a4a",
    seed: "rustic dark loaf of bread, flour dusted",
    img: "../../assets/art/things/bread.png"
  }, {
    name: "Festival cake",
    tag: "Food",
    price: "8c",
    from: "Maris",
    tint: "#d8a85a",
    seed: "honey festival cake, dried fruit",
    img: "../../assets/art/things/steaming-bread.jpg"
  }, {
    name: "Wild mushroom",
    tag: "Forage",
    price: "1c",
    from: "Forage",
    tint: "#8a6b4a",
    seed: "cluster of wild forest mushrooms",
    img: "../../assets/art/things/mushrooms.jpg"
  }, {
    name: "Resin",
    tag: "Forage",
    price: "1c",
    from: "Forage",
    tint: "#a9683a",
    seed: "amber tree resin lump"
  }, {
    name: "Wild herbs",
    tag: "Forage",
    price: "1c",
    from: "Forage",
    tint: "#6b7f5e",
    seed: "bundle of dried green herbs, twine",
    img: "../../assets/art/things/herbs.jpg"
  }, {
    name: "River clay",
    tag: "Material",
    price: "1c",
    from: "Forage",
    tint: "#7a6a52",
    seed: "grey river clay lump"
  }, {
    name: "Whetstone",
    tag: "Tool",
    price: "5c",
    from: "Odran",
    tint: "#5a5a57",
    seed: "worn rectangular whetstone",
    img: "../../assets/art/things/whetstone.jpg"
  }, {
    name: "Road map to Millhaven",
    tag: "Knowledge",
    price: "15c",
    from: "Odran",
    tint: "#cbbf9a",
    seed: "hand-drawn road map, creased parchment",
    img: "../../assets/art/things/map.jpg"
  }, {
    name: "Tinker knowledge map",
    tag: "Knowledge",
    price: "20c",
    from: "Ilya",
    tint: "#caa05a",
    seed: "chalk-marked map, brass pins, shifting roads",
    img: "../../assets/art/things/map.jpg"
  }, {
    name: "Sympathy charm",
    tag: "Ward",
    price: "25c",
    from: "Ilya",
    tint: "#b8863f",
    seed: "brass sympathy charm on cord",
    brass: true,
    img: "../../assets/art/things/talisman.jpg"
  }, {
    name: "Ward pin",
    tag: "Ward",
    price: "6c",
    from: "Ilya",
    tint: "#a9683a",
    seed: "small brass ward pin",
    brass: true,
    img: "../../assets/art/things/talisman-2.png"
  }, {
    name: "Sympathy lamp",
    tag: "Ward",
    price: "—",
    from: "Ilya",
    tint: "#caa05a",
    seed: "small lamp burning a flame you cannot name",
    brass: true
  }, {
    name: "Tallow candle",
    tag: "Light",
    price: "1c",
    from: "Maris",
    tint: "#e8c47a",
    seed: "stub of tallow candle, warm flame",
    img: "../../assets/art/things/candle-stack.jpg"
  }, {
    name: "Travel cloak",
    tag: "Apparel",
    price: "12c",
    from: "Odran",
    tint: "#4a553d",
    seed: "road-worn wool travel cloak"
  }, {
    name: "Iron ladle",
    tag: "Tool",
    price: "3c",
    from: "Maris",
    tint: "#5a5a57",
    seed: "iron bakery ladle"
  }, {
    name: "Mushroom pottage",
    tag: "Craft",
    price: "—",
    from: "Recipe",
    tint: "#7a7048",
    seed: "bowl of mushroom pottage, steam"
  }, {
    name: "Wax-sealed letter",
    tag: "Quest",
    price: "—",
    from: "Notice board",
    tint: "#cbbf9a",
    seed: "wax-sealed letter, militia seal"
  }, {
    name: "Brass tooth",
    tag: "Wrong",
    price: "—",
    from: "Found",
    tint: "#8a7a3a",
    seed: "single brass tooth, uncanny",
    brass: true,
    corrupted: true
  }, {
    name: "Gear-threaded wheat",
    tag: "Wrong",
    price: "—",
    from: "Border",
    tint: "#8fae5a",
    seed: "wheat stalk threaded with tiny brass gears",
    brass: true,
    corrupted: true
  }, {
    name: "Child's gear drawing",
    tag: "Wrong",
    price: "—",
    from: "STIRRING",
    tint: "#9a8f6a",
    seed: "child's charcoal drawing of interlocking gears",
    corrupted: true
  }, {
    name: "Wild berry",
    tag: "Forage",
    price: "1c",
    from: "Forage",
    tint: "#6b3a44",
    seed: "cluster of dark forest berries on the stem"
  }, {
    name: "Honeycomb",
    tag: "Food",
    price: "2c",
    from: "Forage",
    tint: "#d8a85a",
    seed: "broken honeycomb dripping, wax cells"
  }, {
    name: "Goat milk",
    tag: "Food",
    price: "1c",
    from: "Village",
    tint: "#cbbf9a",
    seed: "clay jug of fresh goat milk"
  }, {
    name: "Saint's candle",
    tag: "Light",
    price: "1c",
    from: "Shrine",
    tint: "#e8c47a",
    seed: "votive candle, wax-run stub, faint flame"
  }, {
    name: "Harvest lantern",
    tag: "Light",
    price: "4c",
    from: "Festival",
    tint: "#d6a24a",
    seed: "punched-tin harvest festival lantern, warm glow"
  }, {
    name: "Ward bell",
    tag: "Ward",
    price: "9c",
    from: "Ilya",
    tint: "#b8863f",
    seed: "small brass hand-bell, ward sigil cast in the rim",
    brass: true,
    img: "../../assets/art/things/rune-talisman.jpg"
  }, {
    name: "Brass filings",
    tag: "Wrong",
    price: "—",
    from: "Found",
    tint: "#8a7a3a",
    seed: "pinch of fine brass filings where teeth should be",
    brass: true,
    corrupted: true
  }, {
    name: "Ringing loaf",
    tag: "Wrong",
    price: "—",
    from: "Bakery",
    tint: "#b08a44",
    seed: "split loaf of bread, brass glint in the crumb",
    corrupted: true,
    img: "../../assets/art/things/golden-ring-in-bread.jpg"
  }, {
    name: "Old clock part",
    tag: "Wrong",
    price: "—",
    from: "Found",
    tint: "#7a6a3a",
    seed: "corroded brass clock gear, teeth worn uneven",
    brass: true,
    corrupted: true
  }, {
    name: "Iron knife",
    tag: "Arms",
    price: "7c",
    from: "Odran",
    tint: "#6a6a66",
    seed: "forged iron belt knife, leather grip",
    img: "../../assets/art/things/iron-knife.jpg"
  }, {
    name: "Stone knife",
    tag: "Arms",
    price: "2c",
    from: "Forage",
    tint: "#7a7068",
    seed: "knapped stone blade, cord-wrapped haft",
    img: "../../assets/art/things/stone-knife.png"
  }, {
    name: "Wooden buckler",
    tag: "Arms",
    price: "10c",
    from: "Odran",
    tint: "#6b4a2a",
    seed: "round wooden buckler, iron boss, worn rim",
    img: "../../assets/art/things/wooden-shield.jpg"
  }, {
    name: "Banded shield",
    tag: "Arms",
    price: "18c",
    from: "Millhaven",
    tint: "#5a4a36",
    seed: "small iron-banded shield, militia issue",
    img: "../../assets/art/things/small-shield.png"
  }, {
    name: "Healing poultice",
    tag: "Heal",
    price: "4c",
    from: "Recipe",
    tint: "#7a8a5e",
    seed: "linen bandage and green yarrow poultice",
    img: "../../assets/art/things/bandage-poultice.png"
  }, {
    name: "Yarrow draught",
    tag: "Heal",
    price: "6c",
    from: "Recipe",
    tint: "#6b5a3a",
    seed: "corked draught of herb tincture",
    img: "../../assets/art/things/potion.jpg"
  }, {
    name: "Iron key",
    tag: "Quest",
    price: "—",
    from: "Found",
    tint: "#5a5a57",
    seed: "old iron key, teeth worn, ribbon tied",
    img: "../../assets/art/things/iron-key.jpg"
  }, {
    name: "Copper coins",
    tag: "Coin",
    price: "—",
    from: "Currency",
    tint: "#b07a3a",
    seed: "small stack of copper coins, worn faces",
    img: "../../assets/art/things/coins.jpg"
  }, {
    name: "Bone dice",
    tag: "Coin",
    price: "3c",
    from: "Odran",
    tint: "#cbbf9a",
    seed: "pair of bone dice and a wooden fate rune",
    img: "../../assets/art/things/dice-rune.png"
  }],
  // ---------------------------------------------------------------
  // RUMORS (notice-board chatter) + MURAL fragments (the shrine wall)
  // ---------------------------------------------------------------
  rumors: [{
    text: "Odran swears the road to Millhaven took an extra hour though the sun said otherwise.",
    phase: "stirring"
  }, {
    text: "A stillborn lamb was found with brass filings where its teeth should be.",
    phase: "spreading"
  }, {
    text: "Maris burned a batch of bread that rang like a bell when it cracked.",
    phase: "stirring"
  }, {
    text: "Tinkers are buying old clock parts at twice their weight in copper.",
    phase: "stirring"
  }, {
    text: "The militia recruitment board has fresh nails \u2014 someone expects volunteers.",
    phase: "dormant"
  }, {
    text: "Wheat near the corruption border stands in rows too straight for wind.",
    phase: "spreading"
  }, {
    text: "Children in the square drew gears in the dirt; by morning the drawings were gone.",
    phase: "stirring"
  }],
  // The unfinished mural \u2014 a fragment surfaces as each phase deepens.
  mural: [{
    frag: "a saint with clock-hands where eyes should be",
    phase: "dormant"
  }, {
    frag: "wheat stalks threaded through brass gears",
    phase: "stirring"
  }, {
    frag: "a child offering bread to something underground",
    phase: "stirring"
  }, {
    frag: "the Marches road winding into a wound of light",
    phase: "spreading"
  }, {
    frag: "a village burning in perfect symmetry",
    phase: "consuming"
  }],
  // ---------------------------------------------------------------
  // WEATHER + PHASES (footer + image modifier)
  // ---------------------------------------------------------------
  weather: [{
    key: "clear",
    label: "Clear",
    note: "Honest light"
  }, {
    key: "overcast",
    label: "Overcast",
    note: "Default mood"
  }, {
    key: "mist",
    label: "Mist",
    note: "Forest margin"
  }, {
    key: "rain",
    label: "Rain",
    note: "Millhaven"
  }, {
    key: "wrong_rain",
    label: "Wrong rain",
    note: "Falls upward · STIRRING+",
    corrupted: true
  }],
  phases: [{
    key: "dormant",
    label: "Dormant",
    mood: "Warm linen, moss, honey light",
    ui: "Clean journal; no corruption motifs"
  }, {
    key: "stirring",
    label: "Stirring",
    mood: "Brass accents; shadows too long",
    ui: "Subtle tick motif in dividers"
  }, {
    key: "spreading",
    label: "Spreading",
    mood: "Desaturated greens; sickly chartreuse",
    ui: "Weather widget shows wrong readings"
  }, {
    key: "consuming",
    label: "Consuming",
    mood: "High contrast; clockwork filigree",
    ui: "Letterbox cutscenes; UI stutters 1 frame/min"
  }]
};
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/clockwork-world/data.js", error: String((e && e.message) || e) }); }

__ds_ns.Badge = __ds_scope.Badge;

__ds_ns.Button = __ds_scope.Button;

__ds_ns.ChoiceChip = __ds_scope.ChoiceChip;

__ds_ns.StatLine = __ds_scope.StatLine;

__ds_ns.AssistantBubble = __ds_scope.AssistantBubble;

__ds_ns.DiceToast = __ds_scope.DiceToast;

__ds_ns.ScenePanel = __ds_scope.ScenePanel;

__ds_ns.WorldClock = __ds_scope.WorldClock;

})();
