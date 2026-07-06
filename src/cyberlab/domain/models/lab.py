from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Lab:
    """Represents a CyberLab laboratory."""

    name: str
