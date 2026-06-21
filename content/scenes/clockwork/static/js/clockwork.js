/**
 * Clockwork Dark — scene client (start screen, intro, Socket.IO game)
 */
(function () {
  "use strict";

  const startScreen = document.getElementById("start-screen");
  const startBg = document.getElementById("start-bg");
  const startWordmark = document.getElementById("start-wordmark");
  const startStatus = document.getElementById("start-status");
  const archetypeList = document.getElementById("archetype-list");
  const startBtn = document.getElementById("start-btn");
  const introBtn = document.getElementById("intro-btn");
  const introOverlay = document.getElementById("intro-overlay");
  const introVideo = document.getElementById("intro-video");
  const introSkip = document.getElementById("intro-skip");
  const gameScreen = document.getElementById("game-screen");

  const logEl = document.getElementById("narrative-log");
  const choicesEl = document.getElementById("choices");
  const statusEl = document.getElementById("connection-status");
  const customForm = document.getElementById("custom-form");
  const customText = document.getElementById("custom-text");
  const assistantBubble = document.getElementById("assistant-bubble");
  const assistantText = document.getElementById("assistant-text");
  const assistantForm = document.getElementById("assistant-form");
  const assistantPortrait = document.getElementById("assistant-portrait");
  const assistantWhisper = document.getElementById("assistant-whisper");
  const sceneImage = document.getElementById("scene-image");
  const scenePlaceholder = document.getElementById("scene-placeholder");
  const sceneCaption = document.getElementById("scene-caption");
  const sceneTitle = document.getElementById("scene-title");
  const gearMotif = document.getElementById("gear-motif");
  const phaseChipsEl = document.getElementById("phase-chips");
  const footerMeta = document.getElementById("footer-meta");
  const diceToast = document.getElementById("dice-toast");
  const diceLine = document.getElementById("dice-line");
  const diceVideo = document.getElementById("dice-video");
  const cutsceneOverlay = document.getElementById("cutscene-overlay");
  const cutsceneVideo = document.getElementById("cutscene-video");
  const cutsceneCaption = document.getElementById("cutscene-caption");
  const cutsceneSkip = document.getElementById("cutscene-skip");
  const overlayPanel = document.getElementById("overlay-panel");
  const overlayBody = document.getElementById("overlay-body");
  const overlayTitle = document.getElementById("overlay-title");
  const overlayClose = document.getElementById("overlay-close");
  const overlayBackdrop = document.getElementById("overlay-backdrop");

  const PHASES = ["dormant", "stirring", "spreading", "consuming"];
  const WEATHER = ["Overcast", "Mist", "Clear", "Rain"];
  const DEFAULT_ARCHETYPES = {
    wayfarer: { name: "Wayfarer", note: "Cloak, staff, road boots" },
    hearthkeeper: { name: "Hearthkeeper", note: "Apron, flour, warm colors" },
    tinker: { name: "Tinker-apprentice", note: "Tool belt, brass pins, chalk" },
  };

  let sessionId = null;
  let busy = false;
  let gameStarted = false;
  let selectedArchetype = "wayfarer";
  let assetManifest = null;
  let worldContent = null;
  let activeOverlay = "";
  let diceToastTimer = null;
  let cutsceneTimer = null;
  let captionIndex = 0;
  let captionInterval = null;

  const socket = io();

  function formatClock(state) {
    if (!state) return "Day 1 · 08:00";
    const hour = String(state.world_hour ?? 8).padStart(2, "0");
    return `Day ${state.world_day ?? 1} · ${hour}:00`;
  }

  function formatFooter(state) {
    const phase = state?.evil_phase || "dormant";
    const weather = WEATHER[(state?.world_day ?? 1) % WEATHER.length];
    const timeLabel =
      (state?.world_hour ?? 8) < 12
        ? "Morning"
        : (state?.world_hour ?? 8) < 18
          ? "Afternoon"
          : "Dusk";
    return `${formatClock(state)} · ${timeLabel} · ${weather} · ${phase}`;
  }

  function renderPhaseChips(activePhase) {
    if (!phaseChipsEl) return;
    phaseChipsEl.innerHTML = "";
    PHASES.forEach((phase) => {
      const chip = document.createElement("span");
      chip.className =
        "phase-chip" + (phase === activePhase ? " phase-chip--active" : "");
      chip.textContent = phase;
      chip.setAttribute("aria-current", phase === activePhase ? "true" : "false");
      phaseChipsEl.appendChild(chip);
    });
    document.body.setAttribute("data-phase", activePhase || "dormant");
  }

  function renderArchetypes(archetypes) {
    archetypeList.innerHTML = "";
    Object.entries(archetypes).forEach(([id, arch]) => {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className =
        "archetype-btn" + (id === selectedArchetype ? " archetype-btn--active" : "");
      btn.setAttribute("role", "radio");
      btn.setAttribute("aria-checked", id === selectedArchetype ? "true" : "false");
      btn.innerHTML = `<strong>${arch.name}</strong><span>${arch.note}</span>`;
      btn.addEventListener("click", () => {
        selectedArchetype = id;
        renderArchetypes(archetypes);
      });
      archetypeList.appendChild(btn);
    });
  }

  function applyStartScreenAssets(manifest) {
    const start = manifest.start_screen || {};
    if (start.background_url && startBg) {
      startBg.style.backgroundImage = `url("${start.background_url}")`;
    }
    if (start.wordmark_url && startWordmark) {
      startWordmark.src = start.wordmark_url;
    }
    renderArchetypes(manifest.archetypes || DEFAULT_ARCHETYPES);
  }

  function showIntro() {
    const url =
      assetManifest?.intro?.video_hd_url ||
      assetManifest?.intro?.video_url;
    if (!url) return;
    introVideo.src = url;
    introOverlay.classList.remove("hidden");
    introVideo.play().catch(() => {});
  }

  function hideIntro() {
    introOverlay.classList.add("hidden");
    introVideo.pause();
    introVideo.removeAttribute("src");
  }

  function enterGame() {
    if (gameStarted) return;
    gameStarted = true;
    startScreen.classList.add("hidden");
    gameScreen.classList.remove("hidden");
    hideIntro();
  }

  let streamingEntry = null;
  let streamedThisTurn = false;

  function appendNarration(text) {
    const entry = document.createElement("p");
    entry.className = "narrative-entry";
    entry.textContent = text;
    logEl.appendChild(entry);
    logEl.scrollTop = logEl.scrollHeight;
  }

  function appendNarrationDelta(chunk) {
    if (!streamingEntry) {
      streamingEntry = document.createElement("p");
      streamingEntry.className = "narrative-entry narrative-entry--streaming";
      logEl.appendChild(streamingEntry);
    }
    streamingEntry.textContent += chunk;
    streamedThisTurn = true;
    logEl.scrollTop = logEl.scrollHeight;
  }

  function renderChoices(choices) {
    choicesEl.innerHTML = "";
    (choices || []).forEach((c, idx) => {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "choice-btn";
      btn.textContent = `${idx + 1}. ${c.text}`;
      btn.dataset.choiceId = c.id;
      btn.addEventListener("click", () => submitChoice(c.id));
      choicesEl.appendChild(btn);
    });
  }

  function itemIconUrl(name) {
    const key = (name || "").toLowerCase();
    const items = assetManifest?.items || {};
    const entry = items[key] || Object.values(items).find((i) => (i.name || "").toLowerCase() === key);
    return entry?.image_url || "";
  }

  function hideOverlay() {
    activeOverlay = "";
    if (overlayPanel) overlayPanel.classList.add("hidden");
    if (overlayBody) overlayBody.innerHTML = "";
  }

  function renderOverlay(overlayKey, scene) {
    if (!overlayKey || !overlayBody) {
      hideOverlay();
      return;
    }
    activeOverlay = overlayKey;
    const titles = {
      bakery: "Maris's hearth — baking",
      trade: "Barter with Ilya of the Nine Pins",
      notice: "Notice board",
      shrine: "Shrine of Unnamed Saints",
      militia: "Millhaven gate",
      combat: "Combat",
    };
    overlayTitle.textContent = titles[overlayKey] || scene?.name || "Scene";
    overlayBody.innerHTML = "";

    if (overlayKey === "bakery") {
      overlayBody.innerHTML = `
        <div class="overlay-grid">
          <div>
            <div class="oven-ring"><div class="oven-inner"><div class="oven-time" id="oven-time">07:42</div></div></div>
            <p class="overlay-kicker" style="text-align:center">Oven · loaf</p>
          </div>
          <div>
            <p class="overlay-kicker">Recipes</p>
            <div class="overlay-recipe overlay-recipe--active">
              <strong>Loaf of bread</strong> <span class="overlay-row-price">12m</span>
              <div><span class="overlay-chip">Flour</span><span class="overlay-chip">Water</span><span class="overlay-chip">Salt</span></div>
            </div>
            <div class="overlay-recipe">
              <strong>Mushroom pottage</strong> <span class="overlay-row-price">20m</span>
              <div><span class="overlay-chip">Wild mushroom ×2</span><span class="overlay-chip">Herbs</span></div>
            </div>
            <div class="overlay-recipe">
              <strong>Festival cake</strong> <span class="overlay-row-price">35m</span>
            </div>
            <p style="font-style:italic;color:rgba(214,178,108,.6);margin-top:12px">She hums to keep the gears quiet.</p>
          </div>
        </div>`;
    } else if (overlayKey === "trade") {
      const give = [
        { name: "Wild mushroom", qty: 3, worth: 1 },
        { name: "Resin", qty: 2, worth: 1 },
      ];
      const get = [
        { name: "Sympathy charm", qty: 1, worth: 25 },
        { name: "Tinker knowledge map", qty: 1, worth: 20 },
      ];
      const giveHtml = give.map((g) => `
        <div class="overlay-row">
          <span class="overlay-row-icon"></span>
          <span class="overlay-row-label">${g.name} ×${g.qty}</span>
          <span class="overlay-row-price">${g.worth * g.qty}c</span>
        </div>`).join("");
      const getHtml = get.map((g) => `
        <div class="overlay-row">
          <span class="overlay-row-icon"></span>
          <span class="overlay-row-label">${g.name}</span>
          <span class="overlay-row-price">${g.worth}c</span>
        </div>`).join("");
      overlayBody.innerHTML = `
        <div class="overlay-grid">
          <div><p class="overlay-kicker">You give</p>${giveHtml}</div>
          <div><p class="overlay-kicker">Ilya offers</p>${getHtml}</div>
        </div>
        <div class="overlay-actions">
          <button type="button" class="btn-secondary" data-overlay-action="close">Step back</button>
          <button type="button" class="btn-primary">Strike the bargain</button>
        </div>`;
    } else if (overlayKey === "notice") {
      const rumors = (scene?.rumors || worldContent?.rumors || []).slice(0, 5);
      overlayBody.innerHTML = `
        <p class="overlay-kicker">Village chatter</p>
        <ul>${rumors.map((r) => `<li>${typeof r === "string" ? r : r.text || ""}</li>`).join("")}</ul>
        <p class="overlay-kicker">Militia</p>
        <p>Fresh nails on the recruitment board — someone expects volunteers.</p>`;
    } else if (overlayKey === "shrine") {
      const frag = scene?.mural_fragment || "a saint with clock-hands where eyes should be";
      overlayBody.innerHTML = `
        <p class="overlay-kicker">The unfinished mural</p>
        <div class="overlay-mural">${frag}</div>
        <p style="margin-top:14px;color:var(--text-muted)">Greta Moss tends the candles and refuses to finish the wall.</p>`;
    } else if (overlayKey === "militia") {
      overlayBody.innerHTML = `
        <p>Sergeant Sera meets you under the dripping banner. "The road from the Heartlands is wrong tonight," she says. "I can spare you the gate, or your silence. Not both."</p>
        <div class="overlay-actions" style="justify-content:flex-start;flex-wrap:wrap">
          <button type="button" class="choice-btn">Show your road map</button>
          <button type="button" class="choice-btn">Offer militia letter</button>
          <button type="button" class="choice-btn">Step back from the gate</button>
        </div>`;
    } else if (overlayKey === "combat") {
      const enemies = assetManifest?.enemies || {};
      const foe = enemies.wolf || enemies.scarecrow || {};
      overlayBody.innerHTML = `
        <p class="overlay-kicker">${foe.name || "Threat"}</p>
        ${foe.image_url ? `<img src="${foe.image_url}" alt="" style="width:100%;max-height:200px;object-fit:cover;border-radius:3px" />` : ""}
        <p style="margin-top:12px">${foe.blurb || "Lean and rain-wet. Flee is a real option."}</p>`;
    }

    overlayBody.querySelectorAll("[data-overlay-action='close']").forEach((btn) => {
      btn.addEventListener("click", hideOverlay);
    });
    overlayPanel.classList.remove("hidden");
  }

  function applySceneVisual(scene) {
    if (!scene) return;
    if (scene.name) sceneTitle.textContent = scene.name;
    if (scene.caption) {
      sceneCaption.textContent = scene.caption;
      scenePlaceholder.textContent = scene.caption;
    }
    if (scene.image_url) {
      sceneImage.src = scene.image_url;
      sceneImage.hidden = false;
      scenePlaceholder.hidden = true;
    }
    if (scene.overlay && scene.overlay !== activeOverlay) {
      renderOverlay(scene.overlay, scene);
    } else if (!scene.overlay) {
      hideOverlay();
    }
  }

  function updateStats(state) {
    if (!state || !state.stats) return;
    document.getElementById("stat-hp").textContent =
      `${state.stats.hp}/${state.stats.max_hp}`;
    document.getElementById("stat-stamina").textContent = String(
      state.stats.stamina
    );
    document.getElementById("stat-gold").textContent = String(state.stats.gold);
    document.getElementById("stat-location").textContent =
      state.location_id || "—";
    document.getElementById("world-clock").textContent = formatClock(state);
    footerMeta.textContent = formatFooter(state);
    renderPhaseChips(state.evil_phase || "dormant");

    const inv = document.getElementById("inventory");
    inv.innerHTML = "";
    (state.inventory || []).forEach((item) => {
      const li = document.createElement("li");
      const icon = itemIconUrl(item.name);
      if (icon) {
        li.innerHTML = `<span class="inventory-chip"><img src="${icon}" alt="" />${item.name} ×${item.qty}</span>`;
      } else {
        li.textContent = `${item.name} ×${item.qty}`;
      }
      inv.appendChild(li);
    });
  }

  function applyTurn(payload) {
    if (streamedThisTurn && streamingEntry) {
      // Prose already rendered live; finalize with the authoritative text.
      if (payload.narration) streamingEntry.textContent = payload.narration;
      streamingEntry.classList.remove("narrative-entry--streaming");
    } else if (payload.narration) {
      appendNarration(payload.narration);
    }
    streamingEntry = null;
    streamedThisTurn = false;
    renderChoices(payload.choices);
    updateStats(payload.state);
    if (payload.scene) applySceneVisual(payload.scene);
    if (payload.assistant && payload.assistant.spoke) {
      showAssistant(payload.assistant);
    }
  }

  function showAssistant(asst) {
    assistantBubble.classList.remove("hidden");
    assistantForm.textContent = asst.form || "cat";
    assistantText.textContent = asst.text || "";

    const forms = assetManifest?.assistant_forms || {};
    const formEntry = forms[asst.form] || forms.cat;
    if (formEntry?.image_url && assistantPortrait) {
      assistantPortrait.src = formEntry.image_url;
      assistantPortrait.hidden = false;
    } else if (assistantPortrait) {
      assistantPortrait.hidden = true;
    }
  }

  function showDiceToast(dice) {
    if (!dice || !diceLine) return;
    const rolls = dice.rolls || [];
    const roll = rolls[0] ?? dice.total ?? "?";
    const mod = dice.modifier ? (dice.modifier > 0 ? `+${dice.modifier}` : dice.modifier) : "";
    const reason = dice.reason ? ` — ${dice.reason}` : "";
    diceLine.textContent = `d20: ${roll}${mod} = ${dice.total ?? roll}${reason}`;
    diceLine.className = "dice-line";
    if (dice.critical) diceLine.classList.add("dice-line--critical");
    if (dice.fumble) diceLine.classList.add("dice-line--fumble");

    const videos = assetManifest?.dice_videos || {};
    const faces = assetManifest?.dice_faces || {};
    const rollVal = (dice.rolls && dice.rolls[0]) || dice.total;
    const faceSrc = rollVal && faces[String(rollVal)];
    const videoSrc =
      faceSrc ||
      (dice.critical && videos.critical) ||
      (dice.fumble && videos.fumble) ||
      videos.roll ||
      videos.roll_0;
    if (videoSrc && diceVideo) {
      diceVideo.src = videoSrc;
      diceVideo.hidden = false;
      diceVideo.play().catch(() => {});
    } else if (diceVideo) {
      diceVideo.hidden = true;
    }

    diceToast.classList.remove("hidden");
    clearTimeout(diceToastTimer);
    diceToastTimer = setTimeout(() => {
      diceToast.classList.add("hidden");
      if (diceVideo) {
        diceVideo.pause();
        diceVideo.hidden = true;
      }
    }, 3200);
  }

  function hideCutscene() {
    cutsceneOverlay.classList.add("hidden");
    cutsceneVideo.pause();
    cutsceneVideo.removeAttribute("src");
    clearTimeout(cutsceneTimer);
    clearInterval(captionInterval);
    captionIndex = 0;
  }

  function showCutscene(data) {
    if (!data?.video_url) return;
    cutsceneVideo.src = data.video_url;
    const captions = data.captions || [];
    captionIndex = 0;
    cutsceneCaption.textContent = captions[0] || "";
    cutsceneOverlay.classList.remove("hidden");
    cutsceneVideo.play().catch(() => {});

    if (captions.length > 1) {
      captionInterval = setInterval(() => {
        captionIndex = (captionIndex + 1) % captions.length;
        cutsceneCaption.textContent = captions[captionIndex];
      }, 2800);
    }

    const skipAfter = (data.skip_after_seconds || 5) * 1000;
    clearTimeout(cutsceneTimer);
    cutsceneTimer = setTimeout(hideCutscene, skipAfter + 4000);
  }

  function setBusy(value) {
    busy = value;
    choicesEl.querySelectorAll("button").forEach((b) => {
      b.disabled = value;
    });
  }

  function submitChoice(choiceId, custom) {
    if (!sessionId || busy) return;
    setBusy(true);
    streamingEntry = null;
    streamedThisTurn = false;
    socket.emit("player_choice", {
      session_id: sessionId,
      choice_id: choiceId,
      custom_text: custom || null,
    });
  }

  async function loadWorldContent() {
    try {
      const res = await fetch("/api/world/content");
      worldContent = await res.json();
    } catch (err) {
      console.warn("World content unavailable", err);
    }
  }

  async function loadManifest() {
    try {
      await loadWorldContent();
      const res = await fetch("/api/assets/manifest");
      assetManifest = await res.json();
      applyStartScreenAssets(assetManifest);
      if (assetManifest.design_available && gearMotif) {
        const brand = assetManifest.brand || {};
        if (brand.gear_motif) {
          gearMotif.src = brand.gear_motif;
          gearMotif.hidden = false;
        }
      }
      if (assistantWhisper) {
        assistantWhisper.textContent =
          "Something watches from the stillness without moving.";
      }
      startStatus.textContent = "Ready";
    } catch (err) {
      console.warn("Asset manifest unavailable", err);
      renderArchetypes(DEFAULT_ARCHETYPES);
      startStatus.textContent = "Assets offline — playing with fallbacks";
    }
  }

  async function startGame() {
    enterGame();
    startBtn.disabled = true;
    statusEl.textContent = "Starting…";
    try {
      const res = await fetch("/api/game/new", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          player_name: "Traveler",
          archetype: selectedArchetype,
        }),
      });
      const data = await res.json();
      sessionId = data.session_id;
      socket.emit("join_session", { session_id: sessionId });
      if (data.opening) applyTurn(data.opening);
      updateStats(data.state);
      statusEl.textContent = "Connected";
    } catch (err) {
      statusEl.textContent = "Failed to start game";
      console.error(err);
    } finally {
      startBtn.disabled = false;
    }
  }

  socket.on("connect", () => {
    if (gameStarted) statusEl.textContent = "Connected";
  });

  socket.on("disconnect", () => {
    if (gameStarted) statusEl.textContent = "Disconnected";
  });

  socket.on("game_started", (data) => {
    sessionId = data.session_id;
    if (data.opening) applyTurn(data.opening);
    else updateStats(data.state);
  });

  socket.on("turn_update", (payload) => {
    applyTurn(payload);
    setBusy(false);
  });

  socket.on("assistant_speak", (data) => {
    showAssistant(data);
  });

  socket.on("image_ready", (data) => {
    if (data.url) {
      sceneImage.src = data.url;
      sceneImage.hidden = false;
      scenePlaceholder.hidden = true;
    }
  });

  socket.on("dice_result", (data) => {
    showDiceToast(data);
  });

  socket.on("cutscene_start", (data) => {
    showCutscene(data);
  });

  socket.on("narration_delta", (chunk) => {
    if (typeof chunk === "string") appendNarrationDelta(chunk);
  });

  socket.on("error", (err) => {
    if (gameStarted) statusEl.textContent = err.message || "Error";
    setBusy(false);
  });

  customForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const text = customText.value.trim();
    if (!text) return;
    customText.value = "";
    submitChoice("custom", text);
  });

  startBtn.addEventListener("click", startGame);
  introBtn.addEventListener("click", showIntro);
  introSkip.addEventListener("click", hideIntro);
  introVideo.addEventListener("ended", hideIntro);
  if (cutsceneSkip) cutsceneSkip.addEventListener("click", hideCutscene);
  if (overlayClose) overlayClose.addEventListener("click", hideOverlay);
  if (overlayBackdrop) overlayBackdrop.addEventListener("click", hideOverlay);

  loadManifest();
})();