from __future__ import annotations

from typing import Protocol

from cyberlab.domain.models.lab_execution_report import (
    LabExecutionReport,
)


class LabRunnerProtocol(Protocol):
    """Protocol for laboratory lifecycle management."""

    def run(
        self,
        lab_id: str,
    ) -> LabExecutionReport:
        """Run a laboratory."""

    def stop(
        self,
        lab_id: str,
    ) -> LabExecutionReport:
        """Stop a laboratory."""
