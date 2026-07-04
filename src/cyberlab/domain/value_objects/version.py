from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Version:
    """Represents the CyberLab version."""

    major: int
    minor: int
    patch: int

    @classmethod
    def current(cls) -> Version:
        """Return the current framework version."""
        return cls(0, 1, 0)

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"
