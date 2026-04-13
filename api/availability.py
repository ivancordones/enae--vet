"""Mock availability tool with ENAE clinic constraints."""

from __future__ import annotations

from datetime import datetime


DOG_MINUTES = {
    "male": 30,
    "female": 50,
}


CAT_MINUTES = {
    "male": 12,
    "female": 15,
}


MOCK_DAY_LOAD = {
    "monday": {"minutes_used": 180, "dogs_count": 2},
    "tuesday": {"minutes_used": 120, "dogs_count": 1},
    "wednesday": {"minutes_used": 210, "dogs_count": 1},
    "thursday": {"minutes_used": 90, "dogs_count": 0},
}


def pickup_window(species: str | None) -> str:
    """Returns mandatory pickup/dropoff window by species."""
    if species == "dog":
        return "Dogs must be dropped off strictly between 09:00 and 10:30."
    return "Cats must be dropped off strictly between 08:00 and 09:00."


def surgery_minutes(species: str | None, sex: str | None) -> int:
    """Returns mock surgery duration according to simplified rules."""
    if species == "dog":
        return DOG_MINUTES.get(sex or "female", 50)
    return CAT_MINUTES.get(sex or "female", 15)


def check_mock_availability(
    species: str | None,
    sex: str | None,
    in_heat: bool | None,
    requested_day: str | None,
) -> str:
    """Evaluates booking feasibility with deterministic mock data."""
    if in_heat:
        return (
            "I cannot confirm surgery while the pet is in heat. Please wait until "
            "the heat period ends and ask again for the next available day."
        )

    day_key = (requested_day or datetime.utcnow().strftime("%A")).lower()
    if day_key not in MOCK_DAY_LOAD:
        return (
            "Surgery days are Monday to Thursday. Please choose a day in that "
            "range, and I will check availability."
        )

    minutes_needed = surgery_minutes(species, sex)
    day_state = MOCK_DAY_LOAD[day_key]

    if species == "dog" and day_state["dogs_count"] >= 2:
        return (
            f"{day_key.title()} is full for dogs (daily max 2 dogs). "
            "Please choose another surgery day."
        )

    if day_state["minutes_used"] + minutes_needed > 240:
        return (
            f"{day_key.title()} has no remaining surgical capacity. "
            "Please choose another day."
        )

    return (
        f"{day_key.title()} is available for this procedure. Estimated surgery "
        f"time cost: {minutes_needed} minutes. {pickup_window(species)}"
    )
