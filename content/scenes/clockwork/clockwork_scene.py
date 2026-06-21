"""
Clockwork Scene Server
======================

Flask + Socket.IO frontend for The Clockwork Dark.

Version: v0.1.0 [2026-06-20]
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Optional

from flask import jsonify, render_template, request
from flask_socketio import emit, join_room

from content.scenes.clockwork.clockwork_state import (
    GameSession,
    SessionStore,
    resolve_player_action,
    run_turn,
)
from engine.agents.assistant import AssistantAgent
from engine.agents.storyteller import StorytellerAgent
from engine.config import get_config
from engine.design.assets import manifest_for_client, place_metadata
from engine.game.engine import GameEngine, set_active_engine
from engine.game.saves import list_saves, load_game, save_game
from engine.world.content import content_for_client, location_metadata
from engine.media.stt import transcribe_audio
from engine.scenes.design_routes import register_design_routes
from engine.scenes.flask_scene import FlaskScene

logger = logging.getLogger(__name__)

_SCENE_DIR = Path(__file__).resolve().parent

SCENE_METADATA = {
    "name": "clockwork",
    "display_name": "THE CLOCKWORK DARK",
    "port": 5573,
    "type": "rpg",
}

_store: Optional[SessionStore] = None
_scene: Optional["ClockworkScene"] = None


def get_store() -> SessionStore:
    global _store
    if _store is None:
        _store = SessionStore()
    return _store


def reset_store() -> SessionStore:
    """Clear sessions — for tests."""
    global _store
    _store = SessionStore()
    return _store


class ClockworkScene(FlaskScene):
    """Clockwork Dark play scene."""

    def __init__(self, *, testing: bool = False, llm_fn: Any = None) -> None:
        self.llm_fn = llm_fn
        self.store = get_store()
        super().__init__(
            name="clockwork",
            static_folder=_SCENE_DIR / "static",
            template_folder=_SCENE_DIR / "templates",
            testing=testing,
        )

    def register(self) -> None:
        app = self.app
        socketio = self.socketio
        self.design_enabled = register_design_routes(app)

        @app.get("/")
        def index() -> str:
            return render_template(
                "clockwork.html",
                scene=SCENE_METADATA,
                design_enabled=self.design_enabled,
            )

        @app.get("/api/assets/manifest")
        def api_asset_manifest() -> Any:
            return jsonify(manifest_for_client())

        @app.get("/api/metrics")
        def api_metrics() -> Any:
            from engine.observability import get_oracle

            oracle = get_oracle()
            return jsonify({"metrics": oracle.metrics(), "recent": oracle.recent(20)})

        @app.get("/api/assets/place/<location_id>")
        def api_place(location_id: str) -> Any:
            return jsonify(place_metadata(location_id))

        @app.get("/api/world/content")
        def api_world_content() -> Any:
            return jsonify(content_for_client())

        @app.get("/api/world/location/<location_id>")
        def api_world_location(location_id: str) -> Any:
            meta = location_metadata(location_id)
            meta["image"] = place_metadata(location_id)
            return jsonify(meta)

        @app.get("/api/game/saves")
        def api_list_saves() -> Any:
            return jsonify({"saves": list_saves()})

        @app.post("/api/game/save")
        def api_save_game() -> Any:
            body = request.get_json(silent=True) or {}
            session_id = str(body.get("session_id", ""))
            try:
                session = self.store.require(session_id)
            except KeyError:
                return jsonify({"error": "session not found"}), 404
            meta = save_game(session.engine.state, label=str(body.get("label", "")))
            return jsonify(meta)

        @app.post("/api/game/load")
        def api_load_game() -> Any:
            body = request.get_json(silent=True) or {}
            session_id = str(body.get("session_id", ""))
            try:
                state = load_game(session_id)
            except FileNotFoundError:
                return jsonify({"error": "save not found"}), 404
            engine = GameEngine(state)
            set_active_engine(engine)
            session = GameSession(
                engine=engine,
                storyteller=StorytellerAgent(engine, llm_fn=self.llm_fn),
                assistant=AssistantAgent(engine, llm_fn=self.llm_fn),
            )
            self.store._sessions[state.session_id] = session
            return jsonify({"session_id": state.session_id, "state": state.to_dict()})

        @app.post("/api/game/new")
        def api_new_game() -> Any:
            body = request.get_json(silent=True) or {}
            session = self.store.create(
                player_name=str(body.get("player_name", "Traveler")),
                archetype=str(body.get("archetype", "wayfarer")),
                seed=body.get("seed"),
                llm_fn=self.llm_fn,
            )
            payload = {
                "session_id": session.session_id,
                "state": session.engine.state.to_dict(),
                "opening": session.last_turn,
            }
            return jsonify(payload)

        @app.get("/api/game/state")
        def api_get_state() -> Any:
            session_id = request.args.get("session_id", "")
            try:
                session = self.store.require(session_id)
            except KeyError:
                return jsonify({"error": "session not found"}), 404
            return jsonify({"state": session.engine.state.to_dict()})

        @app.post("/api/game/choice")
        def api_choice() -> Any:
            body = request.get_json(silent=True) or {}
            session_id = str(body.get("session_id", ""))
            try:
                session = self.store.require(session_id)
            except KeyError:
                return jsonify({"error": "session not found"}), 404

            action = resolve_player_action(
                session,
                str(body.get("choice_id", "")),
                body.get("custom_text"),
            )
            turn = run_turn(session, action)
            return jsonify(turn)

        @app.post("/api/voice/transcribe")
        def api_transcribe() -> Any:
            session_id = request.form.get("session_id", "")
            audio = request.files.get("audio")
            if audio is None:
                return jsonify({"error": "audio file required"}), 400
            try:
                session = self.store.require(session_id)
            except KeyError:
                return jsonify({"error": "session not found"}), 404

            set_active_engine(session.engine)
            audio_bytes = audio.read()
            stt = transcribe_audio(audio_bytes)
            assistant = session.assistant.process_voice_input(
                audio_bytes,
                scene_context=session.last_turn.get("narration", ""),
            )
            return jsonify({"stt": stt, "assistant": assistant.to_dict()})

        @socketio.on("connect")
        def on_connect() -> None:
            logger.debug("[clockwork_scene] Client connected (operation=connect)")

        @socketio.on("join_session")
        def on_join(data: dict[str, Any]) -> None:
            session_id = str(data.get("session_id", ""))
            if session_id:
                join_room(session_id)
                try:
                    session = self.store.require(session_id)
                    emit(
                        "game_started",
                        {
                            "session_id": session_id,
                            "state": session.engine.state.to_dict(),
                            "opening": session.last_turn,
                        },
                    )
                except KeyError:
                    emit("error", {"message": "session not found"})

        @socketio.on("player_choice")
        def on_player_choice(data: dict[str, Any]) -> None:
            session_id = str(data.get("session_id", ""))
            try:
                session = self.store.require(session_id)
            except KeyError:
                emit("error", {"message": "session not found"})
                return

            action = resolve_player_action(
                session,
                str(data.get("choice_id", "")),
                data.get("custom_text"),
            )

            def _emit(event: str, payload: dict[str, Any]) -> None:
                emit(event, payload, room=session_id)

            run_turn(session, action, emit_callback=_emit)


def create_app(
    *,
    testing: bool = False,
    llm_fn: Any = None,
) -> tuple[ClockworkScene, Any]:
    """
    Application factory for tests and launcher.

    Returns:
        (ClockworkScene instance, Flask app)
    """
    global _scene
    _scene = ClockworkScene(testing=testing, llm_fn=llm_fn)
    return _scene, _scene.app


def run_scene(*, host: Optional[str] = None, port: Optional[int] = None) -> None:
    """Start clockwork scene from launcher."""
    cfg = get_config()
    scene_cfg = cfg.get("scene.clockwork", {}) or {}
    resolved_host = host or str(scene_cfg.get("host", "0.0.0.0"))
    resolved_port = int(port or scene_cfg.get("port", SCENE_METADATA["port"]))
    scene, _ = create_app()
    logger.info(
        "[clockwork_scene] Starting (operation=run_scene, host=%s, port=%s)",
        resolved_host,
        resolved_port,
    )
    scene.run(host=resolved_host, port=resolved_port)