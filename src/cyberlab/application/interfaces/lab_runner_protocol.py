from __future__ import annotations

from typing import Protocol

from cyberlab.domain.models.lab_execution_report import (
    LabExecutionReport,
)


class LabRunnerProtocol(Protocol):
    """Run a CyberLab laboratory."""

    def run(
        self,
        lab_id: str,
    ) -> LabExecutionReport:
        """Run a laboratory."""
        ...
