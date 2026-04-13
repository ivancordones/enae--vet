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
)


@dataclass
class SessionState:
    """Tracks minimal cross-turn memory for one conversation."""

    turn_count: int = 0
    species: str | None = None
    sex: str | None = None
    pet_age_years: int | None = None
    in_heat: bool | None = None
    last_intent: str | None = None
    notes: list[str] = field(default_factory=list)


def extract_entities(message: str, state: SessionState) -> SessionState:
    """Extracts deterministic entities from user text."""
    text = message.lower()

    for token, species in SPECIES_TERMS.items():
        if token in text:
            state.species = species
            break

    if any(token in text for token in ("female", "hembra", "perra", "gata")):
        state.sex = "female"
    elif any(token in text for token in ("male", "macho", "perro", "gato")):
        state.sex = "male"

    age_match = re.search(r"\b(\d{1,2})\s*(años|anos|years|year)\b", text)
    if age_match:
        state.pet_age_years = int(age_match.group(1))

    if "in heat" in text or "celo" in text:
        if any(flag in text for flag in ("not", "no ", "isn't", "isnt", "without")):
            state.in_heat = False
        else:
            state.in_heat = True

    return state


def classify_intent(message: str) -> str:
    """Classifies the user's message with simple deterministic heuristics."""
    text = message.lower()

    if any(term in text for term in EMERGENCY_TERMS):
        return "emergency"
    if any(term in text for term in BOOKING_TERMS):
        return "booking_or_availability"
    if any(term in text for term in RAG_TERMS):
        return "preop_rag"
    if any(term in text for term in ("human", "agent", "persona", "recepción", "reception")):
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


def as_dict(state: SessionState) -> dict[str, Any]:
    """Serializes session state for safe JSON-like storage."""
    return {
        "turn_count": state.turn_count,
        "species": state.species,
        "sex": state.sex,
        "pet_age_years": state.pet_age_years,
        "in_heat": state.in_heat,
        "last_intent": state.last_intent,
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
        last_intent=data.get("last_intent"),
        notes=list(data.get("notes", [])),
    )
