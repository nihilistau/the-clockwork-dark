---
type: Runbook
title: Run on the Beast (remote endpoints)
description: Point the game at the networked RTX-2060 machine for LLM, images, and voice.
tags: [runbook, remote, config, beast, setup]
resource: config/local.yaml
timestamp: 2026-06-21
---

# Run on the Beast (remote endpoints)

The Clockwork Dark is provider-agnostic and config-driven, so the game can run on
a light box (the i3 NUC) while LLM inference, image generation, and voice run on
the **beast** (RTX 2060 12GB) over the network. Nothing in code changes — only
`config/local.yaml` (gitignored; deep-merges over `config/default.yaml`).

## One file to rule them all
```yaml
# config/local.yaml  (never committed)
lmstudio:
  base_url: "http://<beast-ip>:1234/v1"
  api_key: "<lm-studio-key>"            # or set env LMSTUDIO_API_KEY
  models: { big: "<loaded-model>", small: "<loaded-model>", draft: "<loaded-model>" }
comfyui:
  base_url: "http://<beast-ip>:8188"
  enabled: true
tts: { base_url: "http://<beast-ip>:8600", provider: "voxtral" }
stt: { base_url: "http://<beast-ip>:5051", provider: "voxtral" }
```

## Checklist
1. On the beast: LM Studio server on (Developer → enable, note the API key), a
   chat model loaded; ComfyUI launched ([[install-comfyui]]); Voxtral sidecar up
   ([[install-voxtral]]).
2. Open the relevant firewall ports (1234, 8188, 8600, 5051) on the beast.
3. On the play box: fill `config/local.yaml` as above; run `python launcher.py
   clockwork` and open `http://localhost:5573`.
4. Verify: `GET <beast>/v1/models` returns 200 with your key; a turn streams and
   renders an image; narration speaks.

## Graceful degradation
Any service that's down or `enabled: false` falls back cleanly — text narration,
placeholder images — so the game is always playable, just lower-fidelity. This is
exactly how it runs on the GPU-less i3 today.

Related: [[install-comfyui]], [[install-voxtral]], [[clockwork-architecture]]
