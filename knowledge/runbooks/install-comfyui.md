---
type: Runbook
title: Install & Run ComfyUI (image generation)
description: Stand up ComfyUI's API server so the game can render scenes, portraits, and cutscene frames.
tags: [runbook, comfyui, media, setup]
resource: scripts/install_comfyui.ps1
timestamp: 2026-06-21
---

# Install & Run ComfyUI

ComfyUI renders our location stills, NPC portraits, item icons, and corruption
overlays. The game talks to it over the REST API (`/prompt`, `/history`, `/view`,
`/ws`); prompts are built from `data/procgen_templates/comfyui.yaml` by
`engine/media/comfyui.py`, with a placeholder/manifest fallback when it's off.

## Where to run it
The GPU **beast** (RTX 2060 12GB), locally or over the network — **not** the i3
box. SDXL wants ~8GB VRAM; SD1.5 runs in ~4GB.

## Steps
1. Dry-run the installer to see what it will do:
   ```powershell
   ./scripts/install_comfyui.ps1            # prints plan, downloads nothing
   ```
2. On the GPU machine, actually install + launch:
   ```powershell
   ./scripts/install_comfyui.ps1 -Run -Launch -Model sd15   # or -Model sdxl
   ```
   This downloads the portable build, a base checkpoint, and starts the API on
   `0.0.0.0:8188`.
3. Point the game at it (this machine or the beast) in `config/local.yaml`:
   ```yaml
   comfyui:
     base_url: "http://<comfy-host>:8188"
     enabled: true
   ```
4. Restart the game. Scene/portrait tags (`[IMAGE:...]`) now render real images;
   without it, the game uses the bundled placeholders in `data/assets/manifest.yaml`.

## Notes
- Assets can also be **hand-supplied** (Grok / Claude Design) by dropping files
  into `Design_files/assets/` and mapping them in the manifest — ComfyUI is one
  source, not the only one.
- See [[run-on-the-beast]] for the full remote-endpoint config.

Related: [[install-voxtral]], [[run-on-the-beast]], [[clockwork-architecture]]
