from __future__ import annotations

from cyberlab.application.interfaces.lab_lifecycle_protocol import (
    LabLifeCycleProtocol,
)
from cyberlab.domain.models.lab_logs import LabLogs


class LabLogsUseCase:
    """Show logs for a CyberLab laboratory."""

    def __init__(
        self,
        runner: LabLifeCycleProtocol,
    ) -> None:
        self._runner = runner

    def execute(
        self,
        lab_id: str,
    ) -> LabLogs:
        """Show laboratory logs."""

        return self._runner.logs(lab_id)
