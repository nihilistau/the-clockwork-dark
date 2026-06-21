"""Design asset manifest and static route tests."""

from __future__ import annotations

import re

import pytest

from engine.design.assets import (
    design_url,
    get_asset_manifest,
    get_design_root,
    manifest_for_client,
    place_metadata,
    reset_design_cache,
    resolve_cutscene_video,
    resolve_location_image,
    resolve_placeholder_image,
)


@pytest.fixture(autouse=True)
def _reset_caches():
    reset_design_cache()
    yield
    reset_design_cache()


def test_manifest_loads_places():
    manifest = get_asset_manifest()
    assert "forest_clearing" in manifest.get("places", {})
    assert manifest["places"]["forest_clearing"]["image"]


def test_design_url_builder():
    assert design_url("assets/art/scenes/bakery.jpg") == (
        "/design/assets/art/scenes/bakery.jpg"
    )


def test_resolve_location_image():
    url = resolve_location_image("forest_clearing")
    assert url == "/design/assets/art/scenes/forest-mushroom-ring.jpg"


def test_resolve_placeholder_image_tag():
    url = resolve_placeholder_image("edgewood_square_dusk")
    assert url == "/design/assets/art/scenes/town-scene.jpg"


def test_resolve_cutscene_video():
    url = resolve_cutscene_video("cutscene_consuming_horizon")
    assert url == "/design/assets/video/cutscene-wheatfield.mp4"


def test_place_metadata():
    meta = place_metadata("edgewood_bakery")
    assert meta["name"] == "The Hearth Bakery"
    assert "bakery.jpg" in meta["image_url"]


def test_manifest_for_client():
    client = manifest_for_client()
    assert "places" in client
    assert client["places"]["forest_clearing"]["image_url"]
    assert "cutscenes" in client
    assert client["cutscenes"]["cutscene_stirring_phase"]["video_url"]
    assert client["intro"]["video_url"]
    assert client["start_screen"]["background_url"]
    assert "wayfarer" in client["archetypes"]


@pytest.mark.skipif(
    get_design_root() is None,
    reason="Design_files directory not available on this machine",
)
def test_design_static_route_serves_file():
    from content.scenes.clockwork.clockwork_scene import create_app, reset_store

    reset_store()
    _, app = create_app(testing=True)
    client = app.test_client()
    res = client.get("/design/assets/gear-motif.svg")
    assert res.status_code == 200
    assert b"svg" in res.data.lower() or res.mimetype == "image/svg+xml"


def test_asset_manifest_api():
    from content.scenes.clockwork.clockwork_scene import create_app, reset_store

    reset_store()
    _, app = create_app(testing=True)
    client = app.test_client()
    res = client.get("/api/assets/manifest")
    assert res.status_code == 200
    data = res.get_json()
    assert data["places"]["forest_clearing"]["name"] == "The Forest Clearing"


# --- design-as-default + local-first integration (Phase C) ---------------

# The four type voices vendored under Design_files/assets/fonts/ for offline play.
_VENDORED_FONTS = (
    "EBGaramond-Regular.woff2",
    "EBGaramond-SemiBold.woff2",
    "EBGaramond-Italic.woff2",
    "SourceSans3-Regular.woff2",
    "SourceSans3-SemiBold.woff2",
    "SourceSans3-Bold.woff2",
    "IBMPlexMono-Regular.woff2",
    "IBMPlexMono-Medium.woff2",
    "Nunito-Regular.woff2",
    "Nunito-SemiBold.woff2",
)


def test_design_root_resolves_without_env_var(monkeypatch):
    """Design must be the default: the in-repo bundle resolves even with no
    CLOCKWORK_DESIGN_FILES env var set (config default is the repo-relative path)."""
    monkeypatch.delenv("CLOCKWORK_DESIGN_FILES", raising=False)
    reset_design_cache()
    root = get_design_root()
    assert root is not None
    assert root.name == "Design_files"
    assert root.is_dir()


def _iter_manifest_urls(client: dict) -> list[str]:
    urls: list[str] = []
    for section in ("places", "cutscenes", "assistant_forms", "enemies", "npcs", "items"):
        for entry in client.get(section, {}).values():
            for key in ("image_url", "video_url"):
                if entry.get(key):
                    urls.append(entry[key])
    for mapping in ("dice_videos", "dice_faces", "hud"):
        urls.extend(v for v in client.get(mapping, {}).values() if v)
    urls.append(client["intro"]["video_url"])
    urls.append(client["intro"]["video_hd_url"])
    ss = client["start_screen"]
    urls.extend([ss["background_url"], ss["wordmark_url"], ss["gear_motif_url"]])
    return [u for u in urls if u and u.startswith("/design/")]


def test_manifest_assets_exist_on_disk():
    """Every /design/ URL the client requests must map to a real file —
    guards against dangling manifest entries after asset renames."""
    root = get_design_root()
    assert root is not None
    client = manifest_for_client()
    missing = [u for u in _iter_manifest_urls(client) if not (root / u[len("/design/"):]).exists()]
    assert not missing, f"manifest references missing files: {missing[:10]}"


def test_fonts_vendored_for_local_first():
    """Local-first: the four type families ship as .woff2 and fonts.css points
    at them via @font-face (no active Google Fonts CDN @import)."""
    root = get_design_root()
    assert root is not None
    fonts_dir = root / "assets" / "fonts"
    for name in _VENDORED_FONTS:
        assert (fonts_dir / name).exists(), f"missing vendored font: {name}"

    fonts_css = (root / "tokens" / "fonts.css").read_text(encoding="utf-8")
    assert "@font-face" in fonts_css
    assert "../assets/fonts/EBGaramond-Regular.woff2" in fonts_css
    # The CDN line may remain as a documented fallback, but only inside a comment.
    # Strip /* ... */ comments, then assert no *active* Google Fonts @import remains.
    active_css = re.sub(r"/\*.*?\*/", "", fonts_css, flags=re.DOTALL)
    assert "fonts.googleapis.com" not in active_css, (
        "Google Fonts @import is active; expected self-hosted fonts"
    )


def test_phase_themes_present_for_all_evil_phases():
    """phases.css must define a [data-phase] block for every canon evil phase
    so the UI corruption-creep advances with the engine."""
    root = get_design_root()
    assert root is not None
    phases_css = (root / "tokens" / "phases.css").read_text(encoding="utf-8")
    for phase in ("dormant", "stirring", "spreading", "consuming"):
        assert f'[data-phase="{phase}"]' in phases_css