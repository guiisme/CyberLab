from typing import Protocol

from cyberlab.domain.models.lab_execution_report import (
    LabExecutionReport,
)
from cyberlab.domain.models.lab_logs import LabLogs


class LabLifeCycleProtocol(Protocol):
    """Protocol for laboratory execution."""

    def run(
        self,
        lab_id: str,
    ) -> LabExecutionReport:
        """Run a laboratory."""
        ...

    def stop(self, lab_id: str) -> None:
        """Para os recursos do laboratório (mantém dados/volume)."""
        ...

    def down(self, lab_id: str) -> None:
        """Remove completamente os recursos do laboratório."""
        ...

    def status(self, lab_id: str) -> str:
        """Retorna o estado do laboratório (ex: 'running', 'stopped', 'not found')."""
        ...

    def restart(
        self,
        lab_id: str,
    ) -> None:
        """Restart a laboratory."""
        ...

    def exec(self, lab_id: str, command: str) -> str: ...

    def logs(
        self,
        lab_id: str,
    ) -> LabLogs:
        """View logs for a laboratory."""
        ...

    # Adicione ao LabLifeCycleProtocol
    def check_requirements(self) -> bool:
        """Verifica se as ferramentas necessárias estão instaladas."""
        ...

    def setup_ctf(self, lab_id: str, target_pod: str) -> str: ...
