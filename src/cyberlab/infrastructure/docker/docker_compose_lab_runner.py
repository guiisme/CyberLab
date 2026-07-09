from __future__ import annotations

from pathlib import Path

from cyberlab.application.interfaces.lab_runner_protocol import (
    LabRunnerProtocol,
)
from cyberlab.domain.models.lab_execution_report import (
    LabExecutionReport,
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

        compose_file = self._labs_root / lab_id / "compose.yaml"

        result = self._compose_service.up(
            compose_file,
        )

        return LabExecutionReport(
            lab_id=lab_id,
            success=result.exit_code == 0,
            message=(
                "Laboratory started successfully." if result.exit_code == 0 else result.stderr
            ),
        )
