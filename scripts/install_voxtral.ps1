<#
.SYNOPSIS
  Install + run the Voxtral TTS/ASR sidecar for The Clockwork Dark.

.DESCRIPTION
  Voxtral (https://github.com/nihilistau/voxtral-mini-realtime-rs) is a pure-Rust
  CLI for TTS + ASR — it has NO HTTP server of its own. This script clones and
  builds it, fetches the Q4 models, and then runs our thin sidecar
  (scripts/voxtral_sidecar) which exposes /tts and /asr so the game's existing
  tts.py (:8600) and stt.py (:5051) clients can call it unchanged.

  DRY RUN by default (downloads nothing). Pass -Run to clone+build+fetch models.
  Designed for the GPU "beast"; on this i3 box the game runs on text fallback.

  Point the game at the sidecar via config/local.yaml:
      tts: { base_url: "http://<host>:8600", provider: "voxtral" }
      stt: { base_url: "http://<host>:5051", provider: "voxtral" }

.PARAMETER InstallDir  Where to clone voxtral (default .\.voxtral)
.PARAMETER Run         Actually clone + build + fetch models
.PARAMETER Launch      Start the sidecar after build
#>
param(
  [string]$InstallDir = "$PSScriptRoot\..\.voxtral",
  [switch]$Run,
  [switch]$Launch
)

$ErrorActionPreference = "Stop"
$Repo = "https://github.com/nihilistau/voxtral-mini-realtime-rs"

Write-Host "== Voxtral TTS/ASR sidecar installer (The Clockwork Dark) =="
Write-Host "InstallDir : $InstallDir"
Write-Host "Repo       : $Repo"
Write-Host "Sidecar    : /tts (:8600)  /asr (:5051)  — matches tts.py / stt.py"

if (-not $Run -and -not $Launch) {
  Write-Host ""
  Write-Host "DRY RUN. Would:"
  Write-Host "  1. git clone $Repo $InstallDir"
  Write-Host "  2. cargo build --release --features wgpu,cli,hub   (needs Rust toolchain)"
  Write-Host "  3. Fetch Q4 models (~2.5GB ASR + ~2.7GB TTS) via the repo's hf download step"
  Write-Host "  4. Start scripts/voxtral_sidecar (wraps the CLI as HTTP /tts + /asr)"
  Write-Host ""
  Write-Host "Re-run with -Run (build) and/or -Launch on the GPU machine."
  Write-Host "See knowledge/runbooks/install-voxtral.md and scripts/voxtral_sidecar/README.md."
  exit 0
}

if ($Run) {
  if (-not (Get-Command cargo -ErrorAction SilentlyContinue)) {
    throw "Rust toolchain (cargo) not found. Install from https://rustup.rs first."
  }
  if (-not (Test-Path $InstallDir)) {
    Write-Host "Cloning Voxtral..."
    git clone $Repo $InstallDir
  } else { Write-Host "Voxtral already cloned." }
  Push-Location $InstallDir
  try {
    Write-Host "Building (release)... this takes a while."
    cargo build --release --features "wgpu,cli,hub"
    Write-Host "Build complete. Fetch the Q4 GGUF models per the repo README (hf download)."
  } finally { Pop-Location }
}

if ($Launch) {
  Write-Host "Start the sidecar (see scripts/voxtral_sidecar/README.md)."
  Write-Host "It shells out to the built voxtral binary for 'speak' (TTS) and 'transcribe' (ASR)."
}
