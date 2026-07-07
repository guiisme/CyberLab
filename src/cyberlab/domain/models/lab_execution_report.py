from __future__ import annotations

from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class LabExecutionReport:
    """Result of a laboratory execution."""

    lab_id: str
    success: bool
    message: str
