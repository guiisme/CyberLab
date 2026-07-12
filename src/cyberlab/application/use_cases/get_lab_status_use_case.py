from __future__ import annotations

from cyberlab.application.interfaces.lab_lifecycle_protocol import (
    LabRunnerProtocol,
)
from cyberlab.domain.models.lab_execution_report import (
    LaboratoryStatus,
)


class GetLabStatusUseCase:
    """Return the current status of a CyberLab laboratory."""

    def __init__(
        self,
        status: LabRunnerProtocol,
    ) -> None:
        self._status = status

    def execute(
        self,
        lab_id: str,
    ) -> LaboratoryStatus:
        """Return the current status of a laboratory."""

        return self._status.status(lab_id)
