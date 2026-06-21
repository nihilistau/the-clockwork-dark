"""
Configuration Manager
=====================

Loads YAML config with optional environment overrides.

Version: v0.1.0 [2026-06-20]
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Optional

import yaml

_ROOT = Path(__file__).resolve().parent.parent
_DEFAULT_PATH = _ROOT / "config" / "default.yaml"

_instance: Optional["ConfigManager"] = None


class ConfigManager:
    """Dot-notation config access."""

    def __init__(self, data: dict[str, Any]) -> None:
        self._data = data

    def get(self, path: str, default: Any = None) -> Any:
        """Return nested value by dot path."""
        node: Any = self._data
        for part in path.split("."):
            if not isinstance(node, dict) or part not in node:
                return default
            node = node[part]
        if isinstance(node, str) and node.startswith("${") and node.endswith("}"):
            env_key = node[2:-1]
            return os.environ.get(env_key, default)
        return node


def get_config() -> ConfigManager:
    """Return singleton ConfigManager."""
    global _instance
    if _instance is None:
        with _DEFAULT_PATH.open(encoding="utf-8") as fh:
            data = yaml.safe_load(fh) or {}
        _instance = ConfigManager(data)
    return _instance


def reset_config() -> None:
    """Reset singleton (tests only)."""
    global _instance
    _instance = None