"""World content loader tests."""

from __future__ import annotations

from engine.world.content import (
    content_for_client,
    cutscene_for_location,
    load_world_content,
    overlay_for_location,
    phase_meets_minimum,
    reset_content_cache,
    rumors_for_phase,
    travel_edge_allowed,
)


def test_content_yaml_loaded():
    reset_content_cache()
    content = load_world_content(force=True)
    assert len(content.get("places", [])) >= 12
    assert len(content.get("npcs", [])) >= 8
    assert len(content.get("items", [])) >= 30


def test_phase_gates():
    assert phase_meets_minimum("spreading", "stirring")
    assert not phase_meets_minimum("dormant", "stirring")


def test_travel_edge_forest_to_square():
    ok, _ = travel_edge_allowed("forest_clearing", "edgewood_square", evil_phase="dormant")
    assert ok is True


def test_travel_edge_spreading_gate():
    ok, reason = travel_edge_allowed(
        "marches_road",
        "corruption_border",
        evil_phase="dormant",
    )
    assert ok is False
    assert "spreading" in reason.lower()


def test_overlay_and_cutscene_maps():
    assert overlay_for_location("edgewood_bakery") == "bakery"
    assert overlay_for_location("tinker_caravan") == "trade"
    assert cutscene_for_location("millhaven_gate") == "cutscene_closing_gates"


def test_rumors_for_phase():
    dormant = rumors_for_phase("dormant")
    stirring = rumors_for_phase("stirring")
    assert len(stirring) >= len(dormant)


def test_content_for_client():
    payload = content_for_client()
    assert "places" in payload
    assert "overlay_map" in payload