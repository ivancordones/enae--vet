from __future__ import annotations

from typing import Any

from enae_vet.chatbot.server import create_app


class _FakeChain:
    """Minimal fake chain used to avoid real LLM calls in tests."""

    def __init__(self, reply: str) -> None:
        self._reply = reply

    def invoke(self, inputs: Any) -> str:  # noqa: D401
        """Mimic the LangChain Runnable.invoke API."""
        # The real chain would receive a mapping with an "input" key.
        assert isinstance(inputs, dict)
        assert "input" in inputs
        return self._reply


def test_ask_bot_returns_reply_for_valid_message() -> None:
    app = create_app(chain=_FakeChain("hello from bot"))
    client = app.test_client()

    response = client.post("/ask_bot", json={"message": "Hola"})

    assert response.status_code == 200
    assert response.get_json() == {"reply": "hello from bot"}


def test_ask_bot_rejects_empty_message() -> None:
    app = create_app(chain=_FakeChain("unused"))
    client = app.test_client()

    response = client.post("/ask_bot", json={"message": ""})

    assert response.status_code == 400
    body = response.get_json()
    assert body is not None
    assert "error" in body

