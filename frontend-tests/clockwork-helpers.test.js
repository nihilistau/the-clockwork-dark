/*
 * Unit tests for the pure frontend helpers.
 * Run: cd frontend-tests && npm install && npm test
 */
const {
  escapeHtml,
  challengeView,
} = require("../content/scenes/clockwork/static/js/clockwork-helpers.js");

describe("escapeHtml", () => {
  it("neutralizes the XSS-relevant characters", () => {
    expect(escapeHtml('<img src=x onerror="alert(1)">')).toBe(
      "&lt;img src=x onerror=&quot;alert(1)&quot;&gt;"
    );
  });

  it("escapes ampersands first (no double-encoding traps)", () => {
    expect(escapeHtml("Tom & Jerry <3")).toBe("Tom &amp; Jerry &lt;3");
  });

  it("treats null/undefined as empty string", () => {
    expect(escapeHtml(null)).toBe("");
    expect(escapeHtml(undefined)).toBe("");
  });

  it("stringifies non-strings", () => {
    expect(escapeHtml(42)).toBe("42");
  });
});

describe("challengeView", () => {
  it("never throws on an empty or missing spec", () => {
    expect(() => challengeView()).not.toThrow();
    expect(() => challengeView({})).not.toThrow();
    expect(challengeView({}).kind).toBe("challenge");
  });

  it("skill_gauntlet derives current-step text, meta, and a default option", () => {
    const v = challengeView({
      kind: "skill_gauntlet",
      steps: [{ skill: "nerve", dc: 12, text: "Hold the line" }],
      step: 0,
    });
    expect(v.total).toBe(1);
    expect(v.text).toBe("Hold the line");
    expect(v.meta).toContain("nerve");
    expect(v.meta).toContain("12");
    expect(v.options[0].id).toBe("attempt");
  });

  it("skill_gauntlet clamps step past the end without throwing", () => {
    const v = challengeView({
      kind: "skill_gauntlet",
      steps: [{ skill: "wits", dc: 8, text: "One" }],
      step: 9,
    });
    expect(v.text).toBe("One");
  });

  it("decision_tree pulls the current node's text and options", () => {
    const v = challengeView({
      kind: "decision_tree",
      current: "a",
      nodes: { a: { text: "Pick a door", options: [{ id: "x", text: "Left" }] } },
    });
    expect(v.text).toBe("Pick a door");
    expect(v.options).toEqual([{ id: "x", text: "Left" }]);
  });

  it("puzzle requires an answer and surfaces attempts left", () => {
    const v = challengeView({ kind: "puzzle", prompt: "A riddle", attempts_left: 3 });
    expect(v.answerRequired).toBe(true);
    expect(v.text).toBe("A riddle");
    expect(v.meta).toContain("3");
  });

  it("decision_tree surfaces the current node's scene art + carved clue (set-pieces)", () => {
    const v = challengeView({
      kind: "decision_tree",
      current: "descend",
      nodes: {
        descend: {
          text: "Down into the dark",
          image: "assets/Tunnels/tunnel-entrance-reveal.jpg",
          riddle: "low, and with the water",
          options: [{ id: "enter", text: "Climb down" }],
        },
      },
    });
    expect(v.image).toBe("assets/Tunnels/tunnel-entrance-reveal.jpg");
    expect(v.riddle).toContain("water");
    expect(v.options[0].id).toBe("enter");
  });

  it("dice_table offers a roll option", () => {
    const v = challengeView({ kind: "dice_table", title: "Fate" });
    expect(v.options[0].id).toBe("roll");
    expect(v.text).toBe("Fate");
  });

  it("honors the ChallengeResult.to_dict shape (explicit total_steps/options)", () => {
    const v = challengeView({
      kind: "skill_gauntlet",
      text: "Pre-rendered",
      total_steps: 3,
      step: 1,
      options: [{ id: "attempt", text: "Attempt it" }],
      message: "focus · DC 10",
    });
    expect(v.total).toBe(3);
    expect(v.step).toBe(1);
    expect(v.text).toBe("Pre-rendered");
    expect(v.meta).toBe("focus · DC 10");
  });
});
