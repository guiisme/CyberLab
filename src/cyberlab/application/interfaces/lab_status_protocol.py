from typing import Protocol

from cyberlab.domain.models.laboratory_status import LaboratoryStatus


class LabStatusProtocol(Protocol):
    """Provides the execution status of a laboratory."""

    def status(
        self,
        lab_id: str,
    ) -> LaboratoryStatus:
        """Return the current status of a laboratory."""
        ...
