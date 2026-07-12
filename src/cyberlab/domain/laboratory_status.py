from dataclasses import dataclass

from cyberlab.domain.laboratory_state import LaboratoryState


@dataclass(frozen=True, slots=True)
class LaboratoryStatus:
    """Represents the current status of a laboratory."""

    state: LaboratoryState

    @property
    def is_running(self) -> bool:
        return self.state is LaboratoryState.RUNNING

    @property
    def is_stopped(self) -> bool:
        return self.state is LaboratoryState.STOPPED
