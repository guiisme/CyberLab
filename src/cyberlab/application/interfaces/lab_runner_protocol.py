from typing import Protocol

from cyberlab.domain.models.lab_execution_report import (
    LabExecutionReport,
)


class LabRunnerProtocol(Protocol):
    """Protocol for laboratory execution."""

    def run(
        self,
        lab_id: str,
    ) -> LabExecutionReport:
        """Run a laboratory."""
        ...

    def stop(
        self,
        lab_id: str,
    ) -> LabExecutionReport:
        """Stop a laboratory."""
        ...
