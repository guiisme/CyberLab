from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CheckResult:
    """Represents the result of an environment validation."""

    name: str
    success: bool
    message: str
