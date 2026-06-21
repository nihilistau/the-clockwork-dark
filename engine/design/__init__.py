"""Design system integration — asset manifest and static file resolution."""

from engine.design.assets import (
    design_url,
    get_asset_manifest,
    get_design_root,
    resolve_assistant_image,
    resolve_cutscene_video,
    resolve_location_image,
    resolve_placeholder_image,
)

__all__ = [
    "design_url",
    "get_asset_manifest",
    "get_design_root",
    "resolve_assistant_image",
    "resolve_cutscene_video",
    "resolve_location_image",
    "resolve_placeholder_image",
]