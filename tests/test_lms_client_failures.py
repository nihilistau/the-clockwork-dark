"""LMSClient streaming failure + malformed-SSE handling (mocked HTTP).

Covers the ``chat_stream`` error branch (transport failure -> "error" event +
re-raise) and the JSONDecodeError skip (a bad ``data:`` line must not derail a
good delta).
"""

from __future__ import annotations

import json

import httpx
import pytest

from engine.lmstudio.client import LMSClient, reset_lms_client
from engine.lmstudio.events import LMSStreamEvent


def _bind_transport(client: LMSClient, handler) -> None:
    transport = httpx.MockTransport(handler)
    client._client = httpx.Client(transport=transport, base_url="http://test.local/v1")


def _collect_events() -> tuple[list[LMSStreamEvent], "callable"]:
    events: list[LMSStreamEvent] = []
    return events, events.append


@pytest.mark.parametrize(
    "exc",
    [
        httpx.ConnectError("connection refused"),
        httpx.ReadTimeout("read timed out"),
    ],
)
def test_chat_stream_transport_failure_emits_error_and_reraises(exc):
    reset_lms_client()
    client = LMSClient(base_url="http://test.local/v1")

    def handler(_request: httpx.Request) -> httpx.Response:
        raise exc

    _bind_transport(client, handler)
    events, on_event = _collect_events()

    with pytest.raises(httpx.HTTPError):
        list(
            client.chat_stream(
                [{"role": "user", "content": "hi"}],
                model="test-model",
                on_event=on_event,
            )
        )

    error_events = [e for e in events if e.event_type == "error"]
    assert error_events, "an 'error' LMSStreamEvent must be fired on transport failure"
    assert error_events[0].error
    # no chat.end on the failure path
    assert not any(e.event_type == "chat.end" for e in events)
    client.close()


def test_chat_stream_skips_malformed_sse_line():
    reset_lms_client()
    client = LMSClient(base_url="http://test.local/v1")

    good = json.dumps({"choices": [{"delta": {"content": "Mist rises."}}]})
    body = "\n".join(
        [
            "data: {not valid json at all",   # JSONDecodeError -> skipped
            f"data: {good}",                   # good delta still streams
            "data: [DONE]",
        ]
    ).encode("utf-8")

    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, content=body)

    _bind_transport(client, handler)

    chunks = list(client.chat_stream([{"role": "user", "content": "hi"}], model="m"))
    assert chunks == ["Mist rises."]
    client.close()
