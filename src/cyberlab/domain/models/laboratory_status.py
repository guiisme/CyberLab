from dataclasses import dataclass

from cyberlab.domain.models.laboratory_state import LaboratoryState


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

    def __str__(self) -> str:
        """Return a human-readable representation of the status."""
        return self.state.value
