from __future__ import annotations

from cyberlab.application.interfaces.lab_runner_protocol import (
    LabRunnerProtocol,
)
from cyberlab.domain.models.lab_execution_report import (
    LabExecutionReport,
)


class LabRunUseCase:
    """Run a CyberLab laboratory."""

    def __init__(
        self,
        runner: LabRunnerProtocol,
    ) -> None:
        self._runner = runner

    def execute(
        self,
        lab_id: str,
    ) -> LabExecutionReport:
        """Run a laboratory."""

        return self._runner.run(lab_id)
