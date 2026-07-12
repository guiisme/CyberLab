from __future__ import annotations

from cyberlab.application.interfaces.lab_lifecycle_protocol import (
    LabLifeCycleProtocol,
)
from cyberlab.domain.models.lab_execution_report import (
    LabExecutionReport,
)


class LabStopUseCase:
    """Stop a CyberLab laboratory."""

    def __init__(
        self,
        runner: LabLifeCycleProtocol,
    ) -> None:
        self._runner = runner

    def execute(
        self,
        lab_id: str,
    ) -> LabExecutionReport:
        """Stop a laboratory."""

        return self._runner.stop(lab_id)
