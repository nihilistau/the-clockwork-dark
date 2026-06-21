"""
Design Static Routes
====================

Serve files from the external Design_files tree at /design/...
"""

from __future__ import annotations

import logging
from pathlib import Path

from flask import Flask, Response, send_from_directory

from engine.design.assets import get_design_root

logger = logging.getLogger(__name__)


def register_design_routes(app: Flask) -> bool:
    """
    Register /design/<path> static file route.

    Returns:
        True if design root exists and routes were registered.
    """
    root = get_design_root()
    if root is None:
        logger.info(
            "[design_routes] Skipped — Design_files not found (operation=register)"
        )
        return False

    @app.get("/design/<path:filename>")
    def serve_design(filename: str) -> Response:
        return send_from_directory(str(root), filename)

    logger.info(
        "[design_routes] Registered (operation=register, root=%s)", root
    )
    return True