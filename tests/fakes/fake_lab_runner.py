from __future__ import annotations

from cyberlab.application.interfaces.lab_runner_protocol import (
    LabRunnerProtocol,
)
from cyberlab.domain.models.lab_execution_report import (
    LabExecutionReport,
)


class FakeLabRunner(LabRunnerProtocol):
    """Fake laboratory runner."""

    def __init__(
        self,
        run_reports: dict[str, LabExecutionReport],
        stop_reports: dict[str, LabExecutionReport] | None = None,
    ) -> None:
        self._run_reports = run_reports
        self._stop_reports = stop_reports or {}

        # Mantemos compatibilidade com todos os testes existentes
        self.requested_lab_ids: list[str] = []

        # Preparação para a PR #010
        self.stopped_lab_ids: list[str] = []

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
