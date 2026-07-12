from __future__ import annotations

from pathlib import Path

from cyberlab.application.interfaces.lab_status_protocol import (
    LabStatusProtocol,
)
from cyberlab.domain.models.laboratory_state import (
    LaboratoryState,
)
from cyberlab.domain.models.laboratory_status import (
    LaboratoryStatus,
)
from cyberlab.domain.models.process_result import (
    ProcessResult,
)
from cyberlab.infrastructure.docker.docker_compose_service import (
    DockerComposeService,
)


class DockerComposeLabStatus(LabStatusProtocol):
    """Retrieve laboratory status using Docker Compose."""

    def __init__(
        self,
        compose_service: DockerComposeService,
        labs_root: Path,
    ) -> None:
        self._compose_service = compose_service
        self._labs_root = labs_root

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

    def _compose_file(
        self,
        lab_id: str,
    ) -> Path:
        """Return the Compose file path for a laboratory."""

        return self._labs_root / lab_id / "compose.yaml"

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
