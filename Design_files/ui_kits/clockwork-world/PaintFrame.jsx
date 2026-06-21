/* PaintFrame — a painterly placeholder frame standing in for ComfyUI art.
   Layered earth-gradient + candle bloom + paper grain + an abstract
   CSS silhouette. NOT final art: production stills are generated from
   the prompts shown beside each frame. Keeps everything honest while
   giving each subject a distinct, recognisable mood. */

const { useState: _useState } = React;

function Silhouette({ kind, robe = "#5a6a4a", accent = "#e8c47a", scale = 1 }) {
  const base = { position: "absolute", left: "50%", transform: "translateX(-50%)" };
  const eye = (left) => ({
    position: "absolute", top: 0, left, width: 6 * scale, height: 6 * scale,
    borderRadius: "50%", background: accent, boxShadow: `0 0 ${8 * scale}px ${accent}`,
  });

  if (kind === "cat") {
    return (
      <div style={{ position: "absolute", inset: 0 }}>
        {/* body */}
        <div style={{ ...base, bottom: "8%", width: 120 * scale, height: 90 * scale,
          background: robe, borderRadius: "46% 46% 40% 40% / 60% 60% 40% 40%", filter: "blur(0.4px)" }} />
        {/* ears */}
        <div style={{ ...base, bottom: "44%", marginLeft: -34 * scale, width: 0, height: 0,
          borderLeft: `${14 * scale}px solid transparent`, borderRight: `${10 * scale}px solid transparent`,
          borderBottom: `${26 * scale}px solid ${robe}` }} />
        <div style={{ ...base, bottom: "44%", marginLeft: 34 * scale, width: 0, height: 0,
          borderLeft: `${10 * scale}px solid transparent`, borderRight: `${14 * scale}px solid transparent`,
          borderBottom: `${26 * scale}px solid ${robe}` }} />
        {/* head */}
        <div style={{ ...base, bottom: "30%", width: 76 * scale, height: 64 * scale,
          background: robe, borderRadius: "48% 48% 46% 46%" }} />
        {/* tail */}
        <div style={{ position: "absolute", bottom: "10%", right: "20%", width: 60 * scale, height: 16 * scale,
          background: robe, borderRadius: "50%", transform: "rotate(-28deg)" }} />
        {/* eyes */}
        <div style={{ ...base, bottom: "40%", width: 40 * scale, height: 6 * scale }}>
          <div style={eye(2)} /><div style={eye(32 * scale)} />
        </div>
      </div>
    );
  }

  if (kind === "hood" || kind === "wizard") {
    return (
      <div style={{ position: "absolute", inset: 0 }}>
        {/* robe body */}
        <div style={{ ...base, bottom: 0, width: 150 * scale, height: 170 * scale,
          background: `linear-gradient(180deg, ${robe} 0%, rgba(0,0,0,.55) 120%)`,
          borderRadius: "44% 44% 12% 12% / 70% 70% 12% 12%" }} />
        {/* hood */}
        <div style={{ ...base, bottom: "44%", width: 104 * scale, height: 116 * scale,
          background: robe, borderRadius: "50% 50% 38% 38% / 62% 62% 40% 40%" }} />
        {/* shadowed face */}
        <div style={{ ...base, bottom: "52%", width: 52 * scale, height: 64 * scale,
          background: "radial-gradient(circle at 50% 40%, #0d100c, #14140f)", borderRadius: "50% 50% 46% 46%" }} />
        {/* eyes in shadow */}
        <div style={{ ...base, bottom: "64%", width: 34 * scale, height: 6 * scale }}>
          <div style={eye(0)} /><div style={eye(28 * scale)} />
        </div>
      </div>
    );
  }

  if (kind === "mirror") {
    return (
      <div style={{ position: "absolute", inset: 0 }}>
        <Silhouette kind="person" robe={robe} accent={accent} scale={scale * 0.82} />
        <div style={{ position: "absolute", inset: 0, top: "62%", transform: "scaleY(-1)", opacity: 0.4,
          maskImage: "linear-gradient(180deg, transparent, #000 80%)",
          WebkitMaskImage: "linear-gradient(180deg, transparent, #000 80%)" }}>
          <Silhouette kind="person" robe={accent} accent={robe} scale={scale * 0.82} />
        </div>
      </div>
    );
  }

  if (kind === "mural") {
    // shrine wall: faceless saint arches + a brass gear hint
    const saint = (left) => (
      <div style={{ position: "absolute", bottom: "10%", left, width: 40 * scale, height: 96 * scale,
        background: "linear-gradient(180deg, #2a2418, #14110b)", borderRadius: "50% 50% 8% 8% / 32% 32% 8% 8%",
        boxShadow: "inset 0 2px 6px rgba(232,196,122,.12)" }}>
        {/* missing face */}
        <div style={{ position: "absolute", top: 9 * scale, left: "50%", transform: "translateX(-50%)",
          width: 22 * scale, height: 22 * scale, borderRadius: "50%",
          background: "radial-gradient(circle at 50% 40%, #050604, #0d0b07)" }} />
      </div>
    );
    return (
      <div style={{ position: "absolute", inset: 0 }}>
        {/* wall */}
        <div style={{ position: "absolute", inset: "8% 14% 0", background: "linear-gradient(180deg, #3a3020, #1c1710)",
          borderRadius: "40% 40% 0 0 / 14% 14% 0 0", boxShadow: "inset 0 0 40px rgba(0,0,0,.6)" }} />
        <div style={{ position: "absolute", left: "50%", bottom: 0, transform: "translateX(-50%)", display: "flex", gap: 12 * scale }}>
          {saint(0)}{saint(0)}
        </div>
        {/* brass gear, threaded through the wheat */}
        <div style={{ position: "absolute", top: "20%", left: "50%", transform: "translateX(-50%)",
          width: 30 * scale, height: 30 * scale, borderRadius: "50%",
          border: `${4 * scale}px solid ${accent}`, opacity: 0.7,
          boxShadow: `0 0 ${10 * scale}px ${accent}`, background: "transparent" }} />
      </div>
    );
  }

  if (kind === "barrow") {
    const stone = (left, h) => (
      <div style={{ position: "absolute", bottom: "12%", left, width: 22 * scale, height: h * scale,
        background: "linear-gradient(180deg, #4a4e44, #1c211c)", borderRadius: "44% 44% 6% 6%",
        boxShadow: "inset 0 2px 6px rgba(255,255,255,.06)" }} />
    );
    return (
      <div style={{ position: "absolute", inset: 0 }}>
        {/* mound */}
        <div style={{ position: "absolute", left: "50%", bottom: "6%", transform: "translateX(-50%)",
          width: 200 * scale, height: 90 * scale, background: "linear-gradient(180deg, #2e3a30, #141a14)",
          borderRadius: "50% 50% 12% 12% / 90% 90% 12% 12%" }} />
        {/* doorway */}
        <div style={{ position: "absolute", left: "50%", bottom: "8%", transform: "translateX(-50%)",
          width: 38 * scale, height: 56 * scale, background: "radial-gradient(120% 90% at 50% 100%, #000, #060906)",
          borderRadius: "50% 50% 0 0 / 70% 70% 0 0",
          boxShadow: `inset 0 6px 14px #000, 0 0 ${10 * scale}px ${hexShadow(accent)}` }} />
        {stone("28%", 64)}{stone("66%", 54)}
      </div>
    );
  }

  if (kind === "oven") {
    return (
      <div style={{ position: "absolute", inset: 0 }}>
        {/* stone dome */}
        <div style={{ position: "absolute", left: "50%", bottom: "12%", transform: "translateX(-50%)",
          width: 150 * scale, height: 110 * scale, background: "linear-gradient(180deg, #4a4036, #1f1a14)",
          borderRadius: "50% 50% 14% 14% / 80% 80% 14% 14%", boxShadow: "inset 0 0 40px rgba(0,0,0,.5)" }} />
        {/* fire mouth */}
        <div style={{ position: "absolute", left: "50%", bottom: "16%", transform: "translateX(-50%)",
          width: 58 * scale, height: 40 * scale,
          background: `radial-gradient(120% 100% at 50% 100%, ${accent}, #7a3a10 60%, #1a0d06)`,
          borderRadius: "50% 50% 18% 18% / 64% 64% 18% 18%",
          boxShadow: `0 0 ${24 * scale}px ${accent}` }} />
      </div>
    );
  }

  // person / child
  const s = kind === "child" ? scale * 0.72 : scale;
  return (
    <div style={{ position: "absolute", inset: 0 }}>
      {/* shoulders */}
      <div style={{ ...base, bottom: 0, width: 150 * s, height: 130 * s,
        background: `linear-gradient(180deg, ${robe} 0%, rgba(0,0,0,.5) 130%)`,
        borderRadius: "46% 46% 16% 16% / 64% 64% 16% 16%" }} />
      {/* head */}
      <div style={{ ...base, bottom: "46%", width: 72 * s, height: 86 * s,
        background: robe, borderRadius: "48% 48% 44% 44%" }} />
      {/* face shadow hint */}
      <div style={{ ...base, bottom: "50%", width: 50 * s, height: 60 * s,
        background: "radial-gradient(circle at 50% 38%, rgba(0,0,0,.28), transparent 70%)", borderRadius: "50%" }} />
    </div>
  );
}

function PaintFrame({ tint, glow, caption, sil, robe, accent, corrupted, ratio = "16/9", height, img, imgPos, children }) {
  return (
    <div style={{
      position: "relative", width: "100%", aspectRatio: height ? undefined : ratio,
      height: height || undefined, overflow: "hidden",
      background: tint || "var(--surface-scene)",
      border: "var(--border-rule) solid var(--iron-900)",
      boxShadow: "var(--shadow-card)",
    }}>
      {/* real oil-painted still, when supplied */}
      {img && <div style={{ position: "absolute", inset: 0, backgroundImage: `url("${window.RES(img)}")`,
        backgroundSize: "cover", backgroundPosition: imgPos || "center",
        filter: corrupted ? "saturate(.82)" : "none" }} />}
      {glow && <div className="cw-flicker" style={{ position: "absolute", inset: 0, background: glow, mixBlendMode: "screen", opacity: img ? 0.5 : 1 }} />}
      {/* atmospheric depth — low mist band */}
      <div style={{ position: "absolute", left: 0, right: 0, bottom: 0, height: "42%",
        background: "linear-gradient(0deg, rgba(160,150,120,.10), transparent)", mixBlendMode: "screen" }} />
      {sil && !img && (
        <React.Fragment>
          {/* ground contact shadow */}
          <div style={{ position: "absolute", left: "50%", bottom: "5%", width: "46%", height: 16,
            transform: "translateX(-50%)", borderRadius: "50%",
            background: "radial-gradient(closest-side, rgba(0,0,0,.55), transparent)", filter: "blur(2px)" }} />
          {/* rim-lit figure */}
          <div style={{ position: "absolute", inset: 0,
            filter: `drop-shadow(0 0 1px ${accent || "#d6b26c"}) drop-shadow(0 0 9px ${hexShadow(accent)})` }}>
            <Silhouette kind={sil} robe={robe} accent={accent} />
          </div>
        </React.Fragment>
      )}
      {/* volumetric light ray from above */}
      <div style={{ position: "absolute", top: "-10%", left: "30%", width: "40%", height: "85%",
        background: "linear-gradient(180deg, rgba(214,178,108,.12), transparent 72%)",
        transform: "skewX(-9deg)", mixBlendMode: "screen", pointerEvents: "none" }} />
      {corrupted && <div style={{ position: "absolute", inset: 0, background: "var(--corruption)", opacity: 0.16, mixBlendMode: "color" }} />}
      {/* paper / oil grain */}
      <div style={{ position: "absolute", inset: 0, backgroundImage: "var(--texture-paper)", opacity: img ? 0.32 : 0.55, mixBlendMode: "multiply" }} />
      {/* cinematic vignette */}
      <div style={{ position: "absolute", inset: 0, boxShadow: "inset 0 0 70px 12px rgba(8,9,6,.7)" }} />
      {/* top film lip */}
      <div style={{ position: "absolute", top: 0, left: 0, right: 0, height: 22, background: "linear-gradient(180deg, rgba(6,8,5,.6), transparent)" }} />
      {/* ComfyUI watermark */}
      <span style={{
        position: "absolute", top: 8, right: 10, fontFamily: "var(--font-mono)", fontSize: 10,
        letterSpacing: ".08em", textTransform: "uppercase", color: "rgba(242,232,213,.5)",
      }}>ComfyUI still</span>
      {caption && (
        <span style={{
          position: "absolute", left: 10, bottom: 10, fontFamily: "var(--font-narration)", fontStyle: "italic",
          fontSize: "var(--text-sm)", color: "rgba(242,232,213,.92)", textShadow: "0 1px 3px rgba(0,0,0,.6)",
        }}>{caption}</span>
      )}
      {children}
    </div>
  );
}

window.Silhouette = Silhouette;
window.PaintFrame = PaintFrame;

function hexShadow(hex) {
  if (!hex || hex[0] !== "#") return "rgba(214,178,108,.35)";
  let h = hex.slice(1);
  if (h.length === 3) h = h.split("").map((c) => c + c).join("");
  const n = parseInt(h, 16);
  return `rgba(${(n >> 16) & 255}, ${(n >> 8) & 255}, ${n & 255}, .35)`;
}
