---
type: Runbook
title: Install & Run Voxtral (TTS/ASR voice)
description: Build Voxtral and run the sidecar so narration speaks and the player can talk back.
tags: [runbook, voxtral, voice, tts, asr, setup]
resource: scripts/install_voxtral.ps1
timestamp: 2026-06-21
---

# Install & Run Voxtral

[Voxtral](https://github.com/nihilistau/voxtral-mini-realtime-rs) gives us local
text-to-speech (narration, NPC and Assistant voices) and speech-to-text (player
push-to-talk). It is a pure-Rust **CLI** with no server, so we run a thin
**sidecar** (`scripts/voxtral_sidecar`) that exposes `/tts` and `/asr` matching
the game's `engine/media/tts.py` (:8600) and `stt.py` (:5051) clients.

## Where to run it
The GPU **beast** (Q4 models ~2.5GB ASR + ~2.7GB TTS). On a CPU-only box, leave
it off — the game shows narration as text (`tts.fallback: text`).

## Steps
1. Dry-run:
   ```powershell
   ./scripts/install_voxtral.ps1            # prints plan, downloads nothing
   ```
2. On the GPU machine (needs the Rust toolchain from https://rustup.rs):
   ```powershell
   ./scripts/install_voxtral.ps1 -Run       # clone + cargo build --release
   ```
   Then fetch the Q4 GGUF models per the repo README and start the sidecar
   (`scripts/voxtral_sidecar/README.md`).
3. Point the game at it in `config/local.yaml`:
   ```yaml
   tts: { base_url: "http://<host>:8600", provider: "voxtral" }
   stt: { base_url: "http://<host>:5051", provider: "voxtral" }
   ```

## Voices
Voxtral ships 20 presets across 9 languages — map them to the Storyteller voice
styles (`[VOICE:whisper]` etc.) and the Assistant forms (Grey Wanderer, Cat,
Child, Tinker, Reflection). The realtime WASM build is an option for in-browser
streaming later.

Related: [[install-comfyui]], [[run-on-the-beast]], [[lmstudio-integration-overview]]
