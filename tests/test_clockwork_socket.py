"""Socket layer: streamed narration_delta forwarding + error on bad session.

Covers the Socket.IO ``player_choice`` handler: prose streams to the client as
``narration_delta`` events ahead of the final ``turn_update``, and a bogus
``session_id`` yields an ``error`` event with no ``turn_update``.
"""

from __future__ import annotations

import pytest

# Prose precedes the JSON epilogue so the ProseStreamGate emits a narration_delta.
MOCK_STORYTELLER = """Mist clings to the birch trunks as you step forward.

```json
{
  "tool_calls": [],
  "narration": "Mist clings to the birch trunks as you step forward. Edgewood waits ahead.",
  "choices": [
    {"id": "a", "text": "Walk toward the village"},
    {"id": "b", "text": "Stay in the clearing"}
  ],
  "tags_inline": ""
}
```
"""


@pytest.fixture
def scene_app():
    from content.scenes.clockwork.clockwork_scene import create_app, reset_store

    reset_store()
    scene, app = create_app(testing=True, llm_fn=lambda _messages: MOCK_STORYTELLER)
    app.config["TESTING"] = True
    return scene, app


def test_socket_streams_narration_delta(scene_app):
    scene, app = scene_app
    flask_client = app.test_client()
    session_id = flask_client.post("/api/game/new", json={}).get_json()["session_id"]

    socket_client = scene.socketio.test_client(app, flask_test_client=flask_client)
    socket_client.emit("join_session", {"session_id": session_id})
    socket_client.emit("player_choice", {"session_id": session_id, "choice_id": "a"})

    received = socket_client.get_received()
    names = [e["name"] for e in received]
    assert "narration_delta" in names
    assert "turn_update" in names

    # the streamed prose arrived before the final turn_update
    assert names.index("narration_delta") < names.index("turn_update")

    deltas = [e for e in received if e["name"] == "narration_delta"]
    streamed = "".join(str(d["args"][0]) for d in deltas)
    assert "Mist clings to the birch trunks" in streamed
    # the JSON epilogue is NOT leaked into the streamed prose
    assert "tool_calls" not in streamed
    assert "```" not in streamed


def test_socket_bad_session_emits_error_no_turn_update(scene_app):
    scene, app = scene_app
    flask_client = app.test_client()
    socket_client = scene.socketio.test_client(app, flask_test_client=flask_client)

    socket_client.emit("player_choice", {"session_id": "does-not-exist", "choice_id": "a"})

    received = socket_client.get_received()
    names = [e["name"] for e in received]
    assert "error" in names
    assert "turn_update" not in names
    error = next(e for e in received if e["name"] == "error")
    assert error["args"][0]["message"] == "session not found"
