from __future__ import annotations

from cyberlab.application.interfaces.lab_lifecycle_protocol import (
    LabLifeCycleProtocol,
)
from cyberlab.domain.models.lab_execution_report import (
    LabExecutionReport,
)


class NoOpLabRunner(LabLifeCycleProtocol):
    """No-operation implementation of LabLifeCycleProtocol."""

    def run(
        self,
        lab_id: str,
    ) -> LabExecutionReport:
        """Run a laboratory."""

        return LabExecutionReport(
            lab_id=lab_id,
            success=True,
            message="Laboratory started successfully.",
        )
