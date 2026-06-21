<#
.SYNOPSIS
  Install + launch ComfyUI (image generation) for The Clockwork Dark.

.DESCRIPTION
  Designed to run on the GPU "beast" (RTX 2060 12GB) — NOT this i3 box. By
  default this is a DRY RUN: it prints what it would do and downloads nothing.
  Pass -Run to actually download (~2GB portable + a multi-GB checkpoint) and
  -Launch to start the API server. Heavy downloads are deferred on purpose.

  The game talks to ComfyUI over its REST API (/prompt, /history, /view, /ws)
  at comfyui.base_url. Point the game at this machine via config/local.yaml:
      comfyui:
        base_url: "http://<this-host>:8188"
        enabled: true

.PARAMETER InstallDir   Where to install ComfyUI (default .\.comfyui)
.PARAMETER Model        Base checkpoint: sd15 (4GB, lighter) or sdxl (7GB)
.PARAMETER Run          Actually perform downloads/extraction
.PARAMETER Launch       Start the API server with --listen on port 8188
#>
param(
  [string]$InstallDir = "$PSScriptRoot\..\.comfyui",
  [ValidateSet("sd15","sdxl")][string]$Model = "sd15",
  [switch]$Run,
  [switch]$Launch
)

$ErrorActionPreference = "Stop"
$Port = 8188
$PortableUrl = "https://github.com/comfyanonymous/ComfyUI/releases/latest/download/ComfyUI_windows_portable_nvidia.7z"
$Checkpoints = @{
  sd15 = @{ name = "v1-5-pruned-emaonly.safetensors"; url = "https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned-emaonly.safetensors" }
  sdxl = @{ name = "sd_xl_base_1.0.safetensors";       url = "https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/sd_xl_base_1.0.safetensors" }
}
$ck = $Checkpoints[$Model]

Write-Host "== ComfyUI installer (The Clockwork Dark) =="
Write-Host "InstallDir : $InstallDir"
Write-Host "Model      : $Model ($($ck.name))"
Write-Host "API        : http://0.0.0.0:$Port  (/prompt /history /view /ws)"

if (-not $Run -and -not $Launch) {
  Write-Host ""
  Write-Host "DRY RUN. Would:"
  Write-Host "  1. Download portable build: $PortableUrl"
  Write-Host "  2. Extract to $InstallDir (needs 7-Zip)"
  Write-Host "  3. Download checkpoint -> ComfyUI\models\checkpoints\$($ck.name)"
  Write-Host "     $($ck.url)"
  Write-Host "  4. Launch: python_embeded\python.exe -s ComfyUI\main.py --listen --port $Port"
  Write-Host ""
  Write-Host "Re-run with -Run (download) and/or -Launch (start server) on the GPU machine."
  Write-Host "See knowledge/runbooks/install-comfyui.md and run-on-the-beast.md."
  exit 0
}

if ($Run) {
  New-Item -ItemType Directory -Force -Path $InstallDir | Out-Null
  $archive = Join-Path $InstallDir "comfyui_portable.7z"
  if (-not (Test-Path (Join-Path $InstallDir "ComfyUI"))) {
    Write-Host "Downloading portable build..."
    Invoke-WebRequest -Uri $PortableUrl -OutFile $archive
    $sevenZip = (Get-Command 7z -ErrorAction SilentlyContinue)?.Source
    if (-not $sevenZip) { throw "7-Zip (7z) not found on PATH; install it to extract the portable build." }
    & $sevenZip x $archive "-o$InstallDir" -y | Out-Null
  } else { Write-Host "ComfyUI already present, skipping download." }

  $ckDir = Join-Path $InstallDir "ComfyUI\models\checkpoints"
  New-Item -ItemType Directory -Force -Path $ckDir | Out-Null
  $ckPath = Join-Path $ckDir $ck.name
  if (-not (Test-Path $ckPath)) {
    Write-Host "Downloading checkpoint $($ck.name) (multi-GB)..."
    Invoke-WebRequest -Uri $ck.url -OutFile $ckPath
  } else { Write-Host "Checkpoint already present." }
}

if ($Launch) {
  $py = Join-Path $InstallDir "python_embeded\python.exe"
  $main = Join-Path $InstallDir "ComfyUI\main.py"
  if (-not (Test-Path $py)) { throw "ComfyUI not installed; run with -Run first." }
  Write-Host "Launching ComfyUI API on port $Port ..."
  & $py -s $main --listen --port $Port
}
