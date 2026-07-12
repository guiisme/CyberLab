from __future__ import annotations

from pathlib import Path

from cyberlab.application.interfaces.lab_lifecycle_protocol import (
    LabRunnerProtocol,
)
from cyberlab.domain.models.lab_execution_report import (
    LabExecutionReport,
    LaboratoryState,
    LaboratoryStatus,
)
from cyberlab.domain.models.process_result import (
    ProcessResult,
)
from cyberlab.infrastructure.docker.docker_compose_service import (
    DockerComposeService,
)


class DockerComposeLabRunner(LabRunnerProtocol):
    """Run laboratories using Docker Compose."""

    def __init__(
        self,
        compose_service: DockerComposeService,
        labs_root: Path,
    ) -> None:
        self._compose_service = compose_service
        self._labs_root = labs_root

    def run(
        self,
        lab_id: str,
    ) -> LabExecutionReport:
        """Run a laboratory."""

        compose_file = self._compose_file(
            lab_id,
        )

        result = self._compose_service.up(
            compose_file,
        )

        return self._report(
            lab_id=lab_id,
            result=result,
            success_message="Laboratory started successfully.",
        )

    def stop(
        self,
        lab_id: str,
    ) -> LabExecutionReport:
        """Stop a laboratory."""

        compose_file = self._compose_file(
            lab_id,
        )

        result = self._compose_service.down(
            compose_file,
        )

        return self._report(
            lab_id=lab_id,
            result=result,
            success_message="Laboratory stopped successfully.",
        )

    def status(
        self,
        lab_id: str,
    ) -> LaboratoryStatus:
        """Return the current status of a laboratory."""

        compose_file = self._compose_file(
            lab_id,
        )

        result = self._compose_service.ps(
            compose_file,
        )

        return self._state_from_result(
            result,
        )

    def _state_from_result(
        self,
        result: ProcessResult,
    ) -> LaboratoryStatus:
        """Convert a Docker Compose result into a laboratory status."""

        if result.exit_code != 0:
            return LaboratoryStatus(
                LaboratoryState.STOPPED,
            )

        if "Up" in result.stdout:
            return LaboratoryStatus(
                LaboratoryState.RUNNING,
            )

        return LaboratoryStatus(
            LaboratoryState.STOPPED,
        )

    def restart(
        self,
        lab_id: str,
    ) -> LabExecutionReport:
        """Restart a laboratory."""

        compose_file = self._compose_file(
            lab_id,
        )

        result = self._compose_service.restart(
            compose_file,
        )

        return self._report(
            lab_id=lab_id,
            result=result,
            success_message="Laboratory restarted successfully.",
        )

    def _compose_file(
        self,
        lab_id: str,
    ) -> Path:
        """Return the Compose file path for a laboratory."""

        return self._labs_root / lab_id / "compose.yaml"

    def _report(
        self,
        *,
        lab_id: str,
        result: ProcessResult,
        success_message: str,
    ) -> LabExecutionReport:
        """Build a laboratory execution report."""

        return LabExecutionReport(
            lab_id=lab_id,
            success=result.exit_code == 0,
            message=(success_message if result.exit_code == 0 else result.stderr),
        )
