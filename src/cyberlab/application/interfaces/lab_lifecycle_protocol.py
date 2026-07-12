from typing import Protocol

from cyberlab.domain.models.lab_execution_report import (
    LabExecutionReport,
    LaboratoryStatus,
)


class LabLifeCycleProtocol(Protocol):
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

    def status(
        self,
        lab_id: str,
    ) -> LaboratoryStatus:
        """Return the current status of a laboratory."""
        ...

    def restart(
        self,
        lab_id: str,
    ) -> LabExecutionReport:
        """Restart a laboratory."""
        ...

    def logs(
        self,
        lab_id: str,
    ) -> LabExecutionReport:
        """View logs for a laboratory."""
        ...
