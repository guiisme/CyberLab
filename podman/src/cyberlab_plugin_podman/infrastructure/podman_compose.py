import subprocess
from pathlib import Path

from cyberlab.sdk import (
    LabExecutionReport,
    LabLifeCycleProtocol,
    LabLogs,
    LaboratoryState,
    LaboratoryStatus,
)


class PodmanComposeLabLifecycle(LabLifeCycleProtocol):
    """
    Implementação do ciclo de vida de laboratórios utilizando podman-compose.
    Atua como um adaptador de infraestrutura na Hexagonal Architecture.
    """

    def _resolve_path(self, lab_id: str) -> Path:
        """
        Resolve o caminho do laboratório.
        Nota: Esta implementação é um stub. Idealmente, o adaptador deveria
        receber um LabRepository via injeção de dependência para buscar o path.
        """
        return Path(f"./labs/{lab_id}")

    def run(self, lab_id: str) -> LabExecutionReport:
        """Inicializa o ambiente do laboratório em background."""
        lab_path = self._resolve_path(lab_id)
        subprocess.run(["podman-compose", "up", "-d"], cwd=lab_path, check=True)
        # Retorne a instância correta exigida pelo seu domínio
        return LabExecutionReport(
            lab_id=lab_id, success=True, message="Laboratório iniciado com sucesso via Podman."
        )

    def stop(self, lab_id: str) -> LabExecutionReport:
        """Para e remove os containers e redes do laboratório."""
        lab_path = self._resolve_path(lab_id)
        subprocess.run(["podman-compose", "down"], cwd=lab_path, check=True)
        return LabExecutionReport(
            lab_id=lab_id, success=True, message="Laboratório parado com sucesso via Podman."
        )

    def status(self, lab_id: str) -> LaboratoryStatus:
        """Retorna o status dos containers do laboratório."""
        lab_path = self._resolve_path(lab_id)
        result = subprocess.run(
            ["podman-compose", "ps"], cwd=lab_path, capture_output=True, text=True, check=True
        )

        output = result.stdout.lower()

        # O adaptador traduz a infraestrutura para o domínio
        if "up" in output:
            current_state = LaboratoryState.RUNNING
        elif "exited" in output or "stopped" in output:
            current_state = LaboratoryState.STOPPED
        else:
            current_state = LaboratoryState.UNKNOWN

        return LaboratoryStatus(state=current_state)

    def restart(self, lab_id: str) -> LabExecutionReport:
        """Reinicia os containers e redes do laboratório."""
        lab_path = self._resolve_path(lab_id)
        subprocess.run(["podman-compose", "restart"], cwd=lab_path, check=True)
        return LabExecutionReport(
            lab_id=lab_id, success=True, message="Laboratório reiniciado com sucesso via Podman."
        )

    def logs(self, lab_id: str) -> LabLogs:
        """Coleta os logs do laboratório."""
        lab_path = self._resolve_path(lab_id)
        result = subprocess.run(
            ["podman-compose", "logs"], cwd=lab_path, capture_output=True, text=True, check=True
        )
        return LabLogs(lab_id=lab_id, content=result.stdout)
