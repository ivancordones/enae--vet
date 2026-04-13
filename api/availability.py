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
            f"{day_key.title()} is fully booked with 2 surgeries. "
            "I recommend Tuesday as the next available option."
        )

    if day_state["minutes_used"] + minutes_needed > 240:
        return (
            f"{day_key.title()} has no remaining surgical capacity. "
            "Please choose another day."
        )

    return (
        f"{day_key.title()} is available for this procedure. Estimated surgery "
        f"time: {minutes_needed} minutes. {pickup_window(species)}"
    )


def list_available_days(
    species: str | None,
    sex: str | None,
    in_heat: bool | None,
) -> str:
    """Returns concrete available surgery days (Mon-Thu)."""
    if in_heat:
        return (
            "I cannot confirm dates while the pet is in heat. Please wait around "
            "2 months after heat ends."
        )
    if species is None:
        return "Please confirm species first (dog or cat) so I can provide exact available days."

    minutes_needed = surgery_minutes(species, sex)
    available: list[str] = []
    for day_key, day_state in MOCK_DAY_LOAD.items():
        if species == "dog" and day_state["dogs_count"] >= 2:
            continue
        if day_state["minutes_used"] + minutes_needed > 240:
            continue
        available.append(day_key.title())

    if not available:
        return "No surgery slots are currently available from Monday to Thursday. Please request another week."
    # Keep output realistic: provide a subset instead of all possible days.
    preferred_subset = [day for day in ("Monday", "Tuesday", "Thursday") if day in available]
    days_to_show = preferred_subset if preferred_subset else available[:3]
    if len(days_to_show) == 1:
        return f"We currently have availability next week on {days_to_show[0]}."
    if len(days_to_show) == 2:
        return f"We currently have availability next week on {days_to_show[0]} and {days_to_show[1]}."
    return (
        "We currently have availability next week on "
        f"{days_to_show[0]}, {days_to_show[1]}, and {days_to_show[2]}."
    )
