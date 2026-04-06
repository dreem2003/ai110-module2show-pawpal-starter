from models.priority import Priority

VALID_SPECIES = {"dog", "cat", "rabbit", "bird", "other"}
PRIORITY_MAP: dict[str, Priority] = {
    "low": Priority.LOW,
    "medium": Priority.MEDIUM,
    "high": Priority.HIGH,
}


def validate_duration(minutes: int) -> int:
    """Ensure duration is a positive integer; raise ValueError if not."""
    if minutes < 1:
        raise ValueError(f"Duration must be at least 1 minute, got {minutes}.")
    return minutes


def validate_available_minutes(minutes: int) -> int:
    """Ensure available time is within a sensible daily range (30–840 min)."""
    if not (30 <= minutes <= 840):
        raise ValueError(
            f"Available minutes must be between 30 and 840, got {minutes}."
        )
    return minutes


def validate_species(species: str) -> str:
    """Normalise and validate species string."""
    normalised = species.strip().lower()
    if normalised not in VALID_SPECIES:
        raise ValueError(
            f"Unknown species '{species}'. Expected one of: {', '.join(sorted(VALID_SPECIES))}."
        )
    return normalised


def parse_priority(priority_str: str) -> Priority:
    """Convert a priority string to a Priority enum; raise ValueError if unknown."""
    key = priority_str.strip().lower()
    if key not in PRIORITY_MAP:
        raise ValueError(
            f"Unknown priority '{priority_str}'. Expected one of: {', '.join(PRIORITY_MAP)}."
        )
    return PRIORITY_MAP[key]
