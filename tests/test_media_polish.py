"""
Media-polish wiring
===================

The new cutscene videos resolve through the manifest, and the d20 face stills are
exposed to the client. See data/assets/manifest.yaml, engine/design/assets.py.
"""

from __future__ import annotations

from engine.design.assets import manifest_for_client, resolve_cutscene_video


def test_new_cutscenes_resolve_to_their_videos():
    assert "tunnel-entrance-reveal-video" in (resolve_cutscene_video("cutscene_hidden_tunnel") or "")
    assert "tunnel-stairs-video" in (resolve_cutscene_video("cutscene_tunnel_descent") or "")
    assert "Hollow-Hill-Video-Arrive" in (resolve_cutscene_video("cutscene_hollow_hill") or "")
    assert "Blacksmith-video" in (resolve_cutscene_video("cutscene_forge") or "")


def test_client_manifest_exposes_cutscenes_and_dice_faces():
    m = manifest_for_client()
    assert m["cutscenes"]["cutscene_forge"]["video_url"].startswith("/design/")
    faces = m["dice_faces"]
    assert faces.get("20", "").endswith("dice-d20-20.jpg")
    assert faces.get("1", "").startswith("/design/")


def test_roll_video_url_is_clean():
    # The roll animation filename must not carry a space/paren that breaks the URL.
    roll = manifest_for_client()["dice_videos"]["roll"]
    assert " " not in roll and "(" not in roll
