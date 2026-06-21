"""Phase 4 — ComfyUI/Voxtral setup artifacts + runbooks (PR25)."""

from __future__ import annotations

from pathlib import Path

from engine.okfs import get_bundle, reset_bundle

_ROOT = Path(__file__).resolve().parents[1]


def test_installers_and_sidecar_present():
    assert (_ROOT / "scripts" / "install_comfyui.ps1").exists()
    assert (_ROOT / "scripts" / "install_voxtral.ps1").exists()
    assert (_ROOT / "scripts" / "voxtral_sidecar" / "README.md").exists()


def test_runbooks_in_bundle_and_typed():
    reset_bundle()
    bundle = get_bundle(force=True)
    for slug in ("install-comfyui", "install-voxtral", "run-on-the-beast"):
        c = bundle.get(slug)
        assert c is not None, f"missing runbook concept: {slug}"
        assert c.type == "Runbook"


def test_bundle_still_validates_with_runbooks_and_lore():
    reset_bundle()
    bundle = get_bundle(force=True)
    problems = bundle.validate()
    assert problems == [], f"OKFS bundle problems: {problems[:10]}"
