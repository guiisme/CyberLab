from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class LaboratoryState(StrEnum):
    """Represents the execution state of a laboratory."""

    RUNNING = "running"
    STOPPED = "stopped"
    UNKNOWN = "unkonow"


@dataclass(
    frozen=True,
    slots=True,
)
class LabExecutionReport:
    """Result of a laboratory lifecycle operation."""

    lab_id: str
    success: bool
    message: str


@dataclass(frozen=True, slots=True)
class LaboratoryStatus:
    """Represents the current status of a laboratory."""

    state: LaboratoryState

    @property
    def is_running(self) -> bool:
        """Return whether the laboratory is running."""
        return self.state is LaboratoryState.RUNNING

    @property
    def is_stopped(self) -> bool:
        """Return whether the laboratory is stopped."""
        return self.state is LaboratoryState.STOPPED

    @property
    def is_unknown(self) -> bool:
        """Return whether the laboratory is stopped."""
        return self.state is LaboratoryState.UNKNOWN

    def __str__(self) -> str:
        """Return a human-readable representation of the status."""
        return self.state.value
