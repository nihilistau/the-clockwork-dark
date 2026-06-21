"""
Clockwork Dark Launcher
=======================

Scene launcher — starts Flask + Socket.IO game server.

Version: v0.1.0 [2026-06-20]
"""

from __future__ import annotations

import argparse
import sys


def main(argv: list[str] | None = None) -> int:
    """Entry point for launcher."""
    parser = argparse.ArgumentParser(
        prog="launcher.py",
        description="The Clockwork Dark — scene launcher",
    )
    parser.add_argument(
        "scene",
        nargs="?",
        default="clockwork",
        help="Scene to launch (default: clockwork)",
    )
    parser.add_argument("--list", action="store_true", help="List available scenes")
    parser.add_argument("--port", type=int, default=None, help="Override scene port")
    parser.add_argument("--host", type=str, default=None, help="Override bind host")
    args = parser.parse_args(argv)

    if args.list:
        print("clockwork  —  THE CLOCKWORK DARK  (port 5573)")
        return 0

    if args.scene != "clockwork":
        print(f"Unknown scene: {args.scene}", file=sys.stderr)
        return 1

    from content.scenes.clockwork.clockwork_scene import run_scene

    run_scene(host=args.host, port=args.port)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())