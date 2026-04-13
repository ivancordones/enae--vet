"""Domain rules and intent routing for ENAE VET chatbot."""

from __future__ import annotations

from dataclasses import dataclass, field
import re
from typing import Any


EMERGENCY_TERMS = (
    "urgencia",
    "emergency",
    "sangrado",
    "bleeding",
    "convuls",
    "accidente",
    "seizure",
    "not breathing",
    "no respira",
    "cannot stand",
    "no se levanta",
)


SPECIES_TERMS = {
    "dog": "dog",
    "perro": "dog",
    "perra": "dog",
    "cat": "cat",
    "gato": "cat",
    "gata": "cat",
}


BOOKING_TERMS = (
    "book",
    "booking",
    "schedule",
    "availability",
    "available",
    "cita",
    "agendar",
    "agenda",
    "disponibilidad",
    "fecha",
    "día",
    "dia",
    "when can",
    "next week",
    "thursday",
    "tuesday",
    "lunes",
    "martes",
    "miercoles",
    "miércoles",
    "jueves",
)


RAG_TERMS = (
    "before surgery",
    "before operation",
    "pre-op",
    "preop",
    "instructions",
    "instruction",
    "ayuno",
    "preoperator",
    "comida",
    "agua",
    "food",
    "water",
    "admission",
    "admisión",
    "admision",
    "fast",
    "fasting",
    "ayuno",
)

GENERAL_CONSULT_TERMS = (
    "cough",
    "fever",
    "prescribe",
    "prescription",
    "vomit",
    "diarrhea",
    "diagnosis",
    "tos",
    "fiebre",
    "diagnostico",
    "diagnóstico",
    "recetar",
)


@dataclass
class SessionState:
    """Tracks minimal cross-turn memory for one conversation."""

    turn_count: int = 0
    species: str | None = None
    sex: str | None = None
    pet_age_years: int | None = None
    in_heat: bool | None = None
    booking_intent: bool = False
    handoff_state: bool = False
    last_intent: str | None = None
    missing_fields: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)


def extract_entities(message: str, state: SessionState) -> SessionState:
    """Extracts deterministic entities from user text."""
    text = message.lower()

    for token, species in SPECIES_TERMS.items():
        if re.search(rf"\b{re.escape(token)}s?\b", text):
            state.species = species
            break

    # Sex extraction is intentionally strict:
    # perro/gato can be generic references, so they are not male markers.
    if any(token in text for token in ("female", "hembra", "perra", "gata", "she", "her")):
        state.sex = "female"
    elif any(token in text for token in ("male", "macho", "he", "him")):
        state.sex = "male"

    age_match = re.search(r"\b(\d{1,2})\s*(años|anos|year|years|yr|yrs)\b", text)
    if age_match:
        state.pet_age_years = int(age_match.group(1))

    negative_heat_patterns = (
        r"\bno\s+est[aá]\s+en\s+celo\b",
        r"\bnot\s+in\s+heat\b",
        r"\bisn['’]?t\s+in\s+heat\b",
        r"\bwithout\s+heat\b",
        r"\bsin\s+celo\b",
    )
    positive_heat_patterns = (
        r"\best[aá]\s+en\s+celo\b",
        r"\ben\s+celo\b",
        r"\bin\s+heat\b",
        r"\bcurrently\s+in\s+heat\b",
    )

    if any(re.search(pattern, text) for pattern in negative_heat_patterns):
        state.in_heat = False
    elif any(re.search(pattern, text) for pattern in positive_heat_patterns):
        state.in_heat = True

    if any(token in text for token in BOOKING_TERMS):
        state.booking_intent = True

    if any(token in text for token in ("human", "agent", "persona", "recepción", "recepcion", "asesor")):
        state.handoff_state = True

    state.missing_fields = missing_intake_fields(state)
    return state


def classify_intent(message: str) -> str:
    """Classifies the user's message with simple deterministic heuristics."""
    text = message.lower()

    if any(term in text for term in EMERGENCY_TERMS):
        return "emergency"
    if any(term in text for term in GENERAL_CONSULT_TERMS):
        return "out_of_scope_general_consult"
    if any(term in text for term in RAG_TERMS):
        return "preop_rag"
    if any(term in text for term in ("drop off", "drop-off", "bring my", "entrega", "what about a dog", "what about a cat", "if it were a dog", "if it were a cat")):
        return "query_dropoff_window"
    if any(term in text for term in ("pick up", "pickup", "recoger", "recogida")):
        return "query_pickup_time"
    if any(term in text for term in ("blood test", "analytic", "analítica", "analitica", "required before sterilisation", "required before sterilization", "what if she were", "what if he were", "what if it were")):
        return "query_eligibility"
    if any(term in text for term in ("weekend", "weekends", "fin de semana")):
        return "query_surgery_days"
    if any(term in text for term in BOOKING_TERMS):
        return "booking_or_availability"
    if any(term in text for term in ("human", "agent", "person", "persona", "recepción", "reception")):
        return "handoff_request"
    if any(term in text for term in ("hi", "hello", "hola", "buenas")):
        return "greeting"
    return "sterilization_info"


def analytics_requirement_message(state: SessionState) -> str | None:
    """Returns mandatory pre-op analytics reminder for older pets."""
    if state.pet_age_years is not None and state.pet_age_years > 6:
        return (
            "Because your pet is older than 6 years, preoperative blood analytics "
            "are required before surgery confirmation."
        )
    return None


def build_scope_footer() -> str:
    """Adds a stable domain guardrail footer."""
    return (
        "I can help with sterilization/castration logistics, preparation, and "
        "appointment coordination. For diagnosis or emergencies, I will hand off "
        "to the veterinary team."
    )


def missing_intake_fields(state: SessionState) -> list[str]:
    """Returns ordered missing intake fields."""
    missing: list[str] = []
    if state.species is None:
        missing.append("species")
    if state.sex is None:
        missing.append("sex")
    if state.pet_age_years is None:
        missing.append("age")
    if state.in_heat is None:
        missing.append("in_heat")
    return missing


def next_missing_question(state: SessionState) -> str | None:
    """Returns only the next relevant question for intake."""
    missing = missing_intake_fields(state)
    if not missing:
        return None

    next_field = missing[0]
    if next_field == "species":
        return "What species is your pet (dog or cat)?"
    if next_field == "sex":
        return "Is your pet male or female?"
    if next_field == "age":
        return "How old is your pet in years?"
    return "Is your pet currently in heat?"


def as_dict(state: SessionState) -> dict[str, Any]:
    """Serializes session state for safe JSON-like storage."""
    return {
        "turn_count": state.turn_count,
        "species": state.species,
        "sex": state.sex,
        "pet_age_years": state.pet_age_years,
        "in_heat": state.in_heat,
        "booking_intent": state.booking_intent,
        "handoff_state": state.handoff_state,
        "last_intent": state.last_intent,
        "missing_fields": state.missing_fields,
        "notes": state.notes,
    }


def from_dict(data: dict[str, Any] | None) -> SessionState:
    """Builds a SessionState from an in-memory dictionary."""
    if not data:
        return SessionState()
    return SessionState(
        turn_count=data.get("turn_count", 0),
        species=data.get("species"),
        sex=data.get("sex"),
        pet_age_years=data.get("pet_age_years"),
        in_heat=data.get("in_heat"),
        booking_intent=data.get("booking_intent", False),
        handoff_state=data.get("handoff_state", False),
        last_intent=data.get("last_intent"),
        missing_fields=list(data.get("missing_fields", [])),
        notes=list(data.get("notes", [])),
    )
