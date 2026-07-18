from __future__ import annotations

from pathlib import Path

from cyberlab.application.interfaces.lab_lifecycle_protocol import (
    LabLifeCycleProtocol,
)
from cyberlab.domain.models.lab_execution_report import (
    LabExecutionReport,
    LaboratoryState,
    LaboratoryStatus,
)
from cyberlab.domain.models.lab_logs import LabLogs
from cyberlab.domain.models.process_result import (
    ProcessResult,
)
from cyberlab.infrastructure.docker.docker_compose_service import (
    DockerComposeService,
)


class DockerComposeLabRunner(LabLifeCycleProtocol):
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

    def logs(
        self,
        lab_id: str,
    ) -> LabLogs:
        """View logs for a laboratory."""

        compose_file = self._compose_file(
            lab_id,
        )

        result = self._compose_service.logs(
            compose_file,
        )

        return LabLogs(
            lab_id=lab_id,
            content=(result.stdout if result.exit_code == 0 else result.stderr),
        )

    def exec(self, lab_id: str, command: str) -> str:
        """Execute a command in the first running Compose container."""

        containers = self._compose_service.container_ids(self._compose_file(lab_id))
        if containers.exit_code != 0:
            return f"Erro ao localizar container: {containers.stderr}"

        container_ids = containers.stdout.splitlines()
        if not container_ids:
            return f"Erro ao executar: nenhum container ativo para '{lab_id}'."

        result = self._compose_service.exec(container_ids[0], command)
        if result.exit_code != 0:
            return f"Erro ao executar: {result.stderr}"
        return result.stdout or "(comando executado sem saída)"

    def proxy(self, lab_id: str) -> str:
        """Show host endpoints already published by the Compose laboratory."""

        containers = self._compose_service.container_ids(self._compose_file(lab_id))
        if containers.exit_code != 0:
            return f"Erro ao localizar container: {containers.stderr.strip()}"

        container_ids = containers.stdout.splitlines()
        if not container_ids:
            return f"Nenhum container ativo para '{lab_id}'. Execute 'lab run {lab_id}' primeiro."

        result = self._compose_service.ports(container_ids[0])
        if result.exit_code != 0:
            return f"Erro ao consultar portas: {result.stderr.strip()}"

        ports = result.stdout.strip()
        if not ports:
            return f"O laboratório '{lab_id}' não publica portas no host."
        return f"Endpoint(s) publicado(s) para '{lab_id}':\n{ports}"

    def console(self, lab_id: str, shell: str = "/bin/bash") -> str:
        """Open an interactive Docker console in the first Compose container."""

        containers = self._compose_service.container_ids(self._compose_file(lab_id))
        if containers.exit_code != 0:
            return f"Erro ao localizar container: {containers.stderr.strip()}"

        container_ids = containers.stdout.splitlines()
        if not container_ids:
            return f"Nenhum container ativo para '{lab_id}'. Execute 'lab run {lab_id}' primeiro."

        exit_code = self._compose_service.interactive_shell(container_ids[0], shell)
        if exit_code != 0:
            return f"Console encerrado com código {exit_code}."
        return "Console encerrado."

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
