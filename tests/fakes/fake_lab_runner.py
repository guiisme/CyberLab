from __future__ import annotations

from cyberlab.application.interfaces.lab_runner_protocol import (
    LabRunnerProtocol,
)
from cyberlab.domain.models.lab_execution_report import (
    LabExecutionReport,
)


class FakeLabRunner(LabRunnerProtocol):
    """In-memory implementation of LabRunnerProtocol."""

    def __init__(
        self,
        reports: dict[str, LabExecutionReport],
    ) -> None:
        self._reports = reports
        self.requested_lab_ids: list[str] = []

    def run(
        self,
        lab_id: str,
    ) -> LabExecutionReport:
        """Run a laboratory."""

        self.requested_lab_ids.append(lab_id)

        if lab_id not in self._reports:
            raise AssertionError(f"Unexpected lab id: {lab_id}")

        return self._reports[lab_id]
