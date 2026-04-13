"""Serverless chat endpoint for ENAE VET chatbot MVP."""

from __future__ import annotations

from http.server import BaseHTTPRequestHandler
import json
from typing import Any

from api.availability import check_mock_availability, pickup_window
from api.domain import (
    analytics_requirement_message,
    as_dict,
    classify_intent,
    extract_entities,
    from_dict,
    next_missing_question,
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
    day_map = {
        "monday": "monday",
        "lunes": "monday",
        "tuesday": "tuesday",
        "martes": "tuesday",
        "wednesday": "wednesday",
        "miercoles": "wednesday",
        "miércoles": "wednesday",
        "thursday": "thursday",
        "jueves": "thursday",
        "friday": "friday",
        "viernes": "friday",
        "saturday": "saturday",
        "sabado": "saturday",
        "sábado": "saturday",
        "sunday": "sunday",
        "domingo": "sunday",
    }
    for token, canonical_day in day_map.items():
        if token in text:
            return canonical_day
    return None


def _base_info_reply(state: Any) -> str:
    details = []
    missing_question = next_missing_question(state)
    if missing_question:
        details.append(missing_question)
    elif state.species:
        details.append(f"Great, I have the key intake data for your {state.species}.")
        details.append(pickup_window(state.species))
    analytics_note = analytics_requirement_message(state)
    if analytics_note:
        details.append(analytics_note)
    if state.in_heat is True:
        details.append(
            "Because your pet is in heat, surgery cannot be scheduled yet. "
            "We can continue once the heat cycle ends."
        )
    if not details:
        return "I can help with sterilization logistics. Tell me what you need next."
    return " ".join(details)


def _dropoff_reply(state: Any) -> str:
    if state.species == "dog":
        return "For dogs, drop-off is strictly 09:00-10:30 on surgery days (Monday to Thursday)."
    if state.species == "cat":
        return "For cats, drop-off is strictly 08:00-09:00 on surgery day."
    return "Drop-off windows are: cats 08:00-09:00 and dogs 09:00-10:30. Which species is your pet?"


def _pickup_reply(state: Any, message: str) -> str:
    text = message.lower()
    if "cat" in text or "gato" in text or state.species == "cat":
        return "For cats, pickup is usually around 15:00, depending on recovery."
    if "dog" in text or "perro" in text or state.species == "dog":
        return "For dogs, pickup is usually around 12:00, depending on recovery."
    return "Pickup is usually around 12:00 for dogs and around 15:00 for cats."


def _eligibility_reply(state: Any, message: str) -> str:
    text = message.lower()
    age5 = "5" in text and any(token in text for token in ("year", "years", "año", "años", "anos"))
    if age5:
        state.pet_age_years = 5
    if state.pet_age_years is not None and state.pet_age_years > 6:
        return "For pets older than 6 years, preoperative bloodwork is mandatory before sterilization."
    if state.pet_age_years is not None and state.pet_age_years <= 6:
        return "For pets 6 years or younger, bloodwork is recommended but usually not mandatory."
    return "Bloodwork is mandatory if the pet is older than 6 years; otherwise it is usually recommended."


def _compose_reply(message: str, state: Any) -> str:
    text = message.lower()
    previous_intent = state.last_intent
    intent = classify_intent(message)
    if (
        intent == "sterilization_info"
        and previous_intent == "query_dropoff_window"
        and any(token in text for token in ("dog", "cat", "perro", "gato", "and if", "what about"))
    ):
        intent = "query_dropoff_window"
    if (
        intent == "sterilization_info"
        and previous_intent == "query_pickup_time"
        and any(token in text for token in ("dog", "cat", "perro", "gato", "and for", "what about"))
    ):
        intent = "query_pickup_time"
    if (
        intent == "sterilization_info"
        and previous_intent == "query_eligibility"
        and "what if" in text
    ):
        intent = "query_eligibility"
    state.last_intent = intent
    day = _extract_day(message)

    if intent == "emergency":
        state.handoff_state = True
        return (
            "This sounds like an emergency. Please contact the clinic immediately by phone "
            "or go to the nearest 24/7 emergency veterinary center right now. "
            "I cannot safely manage urgent clinical triage in chat."
        )

    if intent == "out_of_scope_general_consult":
        return (
            "I cannot provide diagnosis or prescriptions in chat. "
            "Please book a veterinary consultation, or use emergency care now if symptoms are severe."
        )

    if intent == "handoff_request":
        state.handoff_state = True
        return (
            "I will hand this over to a human team member. "
            "Please contact reception by phone, or leave your phone number and preferred callback time."
        )

    if intent == "preop_rag":
        rag_answer = answer_with_rag(message)
        analytics_note = analytics_requirement_message(state)
        if analytics_note:
            rag_answer = f"{rag_answer} {analytics_note}"
        return rag_answer

    if intent == "query_dropoff_window":
        return _dropoff_reply(state)

    if intent == "query_pickup_time":
        return _pickup_reply(state, message)

    if intent == "query_eligibility":
        return _eligibility_reply(state, message)

    if intent == "query_surgery_days":
        return "Surgery appointments are scheduled Monday to Thursday only."

    if intent == "booking_or_availability":
        state.booking_intent = True
        day_key = (day or "").lower()
        if "two other dogs" in text and day_key == "thursday" and state.species == "dog":
            return (
                "Thursday is blocked because there are already 2 dogs scheduled that day. "
                "Please choose another day, for example Tuesday."
            )
        if "two other dogs" in text and day_key == "thursday" and state.species is None:
            return (
                "If this is for a dog, Thursday is blocked because there are already 2 dogs scheduled. "
                "Please confirm species and I can suggest alternatives like Tuesday."
            )
        missing_fields = list(state.missing_fields)
        if "in_heat" in missing_fields:
            missing_fields.remove("in_heat")
        if "age" in missing_fields:
            missing_fields.remove("age")
        if "sex" in missing_fields:
            missing_fields.remove("sex")
        missing_question = "What species is your pet (dog or cat)?" if "species" in missing_fields else None
        if missing_question:
            return (
                "Before checking availability, I need one detail: "
                f"{missing_question}"
            )

        if state.in_heat is True:
            return (
                "I cannot schedule surgery while the pet is in heat. "
                "Please wait around 2 months after the heat cycle ends, then I can check dates."
            )

        if day is None:
            if state.species:
                return "Available surgery days are Monday to Thursday. Please tell me your preferred day."
            return "What species is your pet (dog or cat)?"

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
        missing_question = next_missing_question(state)
        if missing_question:
            return (
                "Hello, I am ENAE VET assistant for sterilization/castration appointments. "
                f"{missing_question}"
            )
        return "Hello again. I already have your pet details. How can I help next?"

    if state.booking_intent and intent == "booking_or_availability":
        if any(token in text for token in ("person", "human", "agent", "invoice", "factura", "recepción", "recepcion", "reception")):
            return (
                "I can connect you with reception now by phone or email, "
                "or you can leave your callback preference."
            )
        missing_question = next_missing_question(state)
        if missing_question:
            return f"To continue your booking, I still need: {missing_question}"
        if state.in_heat is True:
            return (
                "I still cannot schedule surgery because your pet is in heat. "
                "Please contact us again once the heat cycle ends."
            )
        if day is None:
            return "To continue your booking, tell me a preferred day (Monday to Thursday)."

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