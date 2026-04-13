"""Serverless chat endpoint for ENAE VET chatbot MVP."""

from __future__ import annotations

from http.server import BaseHTTPRequestHandler
import json
from typing import Any

from api.availability import check_mock_availability, pickup_window
from api.domain import (
    analytics_requirement_message,
    as_dict,
    build_scope_footer,
    classify_intent,
    extract_entities,
    from_dict,
)
from api.rag import answer_with_rag


SESSION_STORE: dict[str, dict[str, Any]] = {}


def _json_response(handler: BaseHTTPRequestHandler, payload: dict[str, Any], status: int = 200) -> None:
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json")
    handler.end_headers()
    handler.wfile.write(json.dumps(payload).encode("utf-8"))


def _extract_day(message: str) -> str | None:
    text = message.lower()
    for day in ("monday", "tuesday", "wednesday", "thursday", "friday", "sábado", "sabado", "saturday", "sunday"):
        if day in text:
            return day
    return None


def _base_info_reply(state: Any) -> str:
    species_text = state.species or "your pet"
    details = [
        f"I can guide you through sterilization for {species_text}.",
        "Please share species, sex, age, and whether the pet is in heat so I can assess requirements.",
    ]
    if state.species:
        details.append(pickup_window(state.species))
    analytics_note = analytics_requirement_message(state)
    if analytics_note:
        details.append(analytics_note)
    details.append(build_scope_footer())
    return " ".join(details)


def _compose_reply(message: str, state: Any) -> str:
    intent = classify_intent(message)
    state.last_intent = intent
    day = _extract_day(message)

    if intent == "emergency":
        return (
            "This sounds like an emergency. Please contact the clinic immediately by phone "
            "or go to the nearest 24/7 emergency veterinary center right now. "
            "I cannot safely manage urgent clinical triage in chat."
        )

    if intent == "handoff_request":
        return (
            "I will hand this over to a human team member. Please leave your phone number, "
            "pet species, and preferred callback time, and reception will contact you."
        )

    if intent == "preop_rag":
        rag_answer = answer_with_rag(message)
        analytics_note = analytics_requirement_message(state)
        if analytics_note:
            rag_answer = f"{rag_answer} {analytics_note}"
        return rag_answer

    if intent == "booking_or_availability":
        availability_result = check_mock_availability(
            species=state.species,
            sex=state.sex,
            in_heat=state.in_heat,
            requested_day=day,
        )
        return (
            f"{availability_result} If you want, I can continue with human handoff "
            "to finalize this booking."
        )

    if intent == "greeting":
        return (
            "Hello, I am ENAE VET assistant for sterilization/castration appointments. "
            "Tell me your pet species, sex, age, and if the pet is currently in heat."
        )

    return _base_info_reply(state)


class handler(BaseHTTPRequestHandler):
    """Vercel-compatible API handler."""

    def do_POST(self) -> None:
        try:
            content_length = int(self.headers.get("Content-Length", "0"))
            raw_body = self.rfile.read(content_length) if content_length > 0 else b"{}"
            body = json.loads(raw_body.decode("utf-8"))
        except Exception:
            _json_response(self, {"response": "Invalid JSON payload."}, status=400)
            return

        message = str(body.get("message", "")).strip()
        session_id = str(body.get("session_id", "")).strip()

        if not message:
            _json_response(self, {"response": "Please provide a message."}, status=400)
            return
        if not session_id:
            _json_response(self, {"response": "Please provide session_id."}, status=400)
            return

        state = from_dict(SESSION_STORE.get(session_id))
        state.turn_count += 1
        state = extract_entities(message, state)

        response_text = _compose_reply(message, state)
        SESSION_STORE[session_id] = as_dict(state)
        _json_response(self, {"response": response_text})

    def do_GET(self) -> None:
        _json_response(
            self,
            {
                "response": (
                    "ENAE VET chat endpoint is running. Use POST with "
                    "session_id and message."
                )
            },
        )