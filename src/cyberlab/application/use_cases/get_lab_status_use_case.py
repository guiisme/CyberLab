from cyberlab.application.interfaces.lab_status_protocol import (
    LabStatusProtocol,
)
from cyberlab.domain.models.laboratory_status import LaboratoryStatus


class GetLabStatusUseCase:
    """Return the current status of a CyberLab laboratory."""

    def __init__(
        self,
        status: LabStatusProtocol,
    ) -> None:
        self._status = status

    def execute(
        self,
        lab_id: str,
    ) -> LaboratoryStatus:
        """Return the current status of a laboratory."""

        return self._status.status(lab_id)
