from __future__ import annotations

from cyberlab.application.interfaces.lab_lifecycle_protocol import (
    LabRunnerProtocol,
)
from cyberlab.domain.models.lab_execution_report import (
    LabExecutionReport,
    LaboratoryState,
    LaboratoryStatus,
)


class FakeLabRunner(LabRunnerProtocol):
    """Fake implementation of LabRunnerProtocol for tests."""

    def __init__(
        self,
        run_reports: dict[str, LabExecutionReport],
        stop_reports: dict[str, LabExecutionReport] | None = None,
        restart_reports: dict[str, LabExecutionReport] | None = None,
        status_to_return: LaboratoryStatus | None = None,
    ) -> None:
        self._run_reports = run_reports
        self._stop_reports = stop_reports or {}
        self._restart_reports = restart_reports or {}
        self.status_to_return = status_to_return or LaboratoryStatus(
            LaboratoryState.STOPPED,
        )

        self.requested_lab_ids: list[str] = []
        self.stopped_lab_ids: list[str] = []
        self.restarted_lab_ids: list[str] = []
        self.received_lab_id: str | None = None

    def run(
        self,
        lab_id: str,
    ) -> LabExecutionReport:
        self.requested_lab_ids.append(
            lab_id,
        )

        if lab_id not in self._run_reports:
            raise AssertionError(f"Unexpected lab id: {lab_id}")

        return self._run_reports[lab_id]

    def stop(
        self,
        lab_id: str,
    ) -> LabExecutionReport:
        self.stopped_lab_ids.append(
            lab_id,
        )

        if lab_id not in self._stop_reports:
            raise AssertionError(f"Unexpected lab id: {lab_id}")

        return self._stop_reports[lab_id]

    def status(
        self,
        lab_id: str,
    ) -> LaboratoryStatus:
        self.received_lab_id = lab_id
        return self.status_to_return

    def restart(
        self,
        lab_id: str,
    ) -> LabExecutionReport:
        self.restarted_lab_ids.append(
            lab_id,
        )

        if lab_id not in self._restart_reports:
            raise AssertionError(f"Unexpected lab id: {lab_id}")

        return self._restart_reports[lab_id]
