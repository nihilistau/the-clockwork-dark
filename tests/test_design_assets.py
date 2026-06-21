"""Design asset manifest and static route tests."""

from __future__ import annotations

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