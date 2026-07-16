import shutil
import subprocess
from pathlib import Path

from cyberlab.sdk import (
    LabExecutionError,
    LabExecutionReport,
    LabLifeCycleProtocol,
    LabLogs,
    LaboratoryState,
    LaboratoryStatus,
)


class PodmanComposeLabLifecycle(LabLifeCycleProtocol):
    """
    Adaptador de infraestrutura para execução de laboratórios via podman-compose.
    Implementa a Arquitetura Hexagonal: isola o subprocesso de infraestrutura
    do domínio de negócio.
    """

    def _resolve_path(self, lab_id: str) -> Path:
        """Resolve o caminho absoluto real na máquina."""
        # Garante que pegamos o caminho completo a partir da raiz do sistema
        return (Path.cwd() / lab_id).resolve()

    def _check_binary(self) -> None:
        if not shutil.which("podman-compose"):
            raise LabExecutionError(
                "O binário 'podman-compose' não foi encontrado no PATH. "
                "Por favor, instale-o com: sudo apt install podman-compose"
            )

    def run(self, lab_id: str) -> LabExecutionReport:
        lab_path = self._resolve_path(lab_id)
        compose_file = lab_path / "docker-compose.yml"

        try:
            # Caminho absoluto para o binário e para o arquivo
            subprocess.run(
                ["/usr/bin/podman-compose", "-f", str(compose_file), "up", "-d"],
                cwd=str(lab_path),
                capture_output=True,
                text=True,
                check=True,
            )
            return LabExecutionReport(
                lab_id=lab_id, success=True, message="Lab iniciado com sucesso."
            )
        except subprocess.CalledProcessError as e:
            # Isso vai te mostrar exatamente o erro do Podman
            raise LabExecutionError(f"Erro no Podman: {e.stderr.strip()}") from e

    def stop(self, lab_id: str) -> LabExecutionReport:
        """Para e remove os containers e redes do laboratório."""
        lab_path = self._resolve_path(lab_id)
        try:
            subprocess.run(
                ["podman-compose", "-f", "docker-compose.yml", "down"],
                cwd=lab_path,
                capture_output=True,
                text=True,
                check=True,
            )
            return LabExecutionReport(
                lab_id=lab_id, success=True, message="Laboratório parado com sucesso via Podman."
            )
        except subprocess.CalledProcessError as e:
            raise LabExecutionError(
                f"Falha ao parar o laboratório '{lab_id}'.\nErro: {e.stderr.strip()}"
            ) from e

    def status(self, lab_id: str) -> LaboratoryStatus:
        lab_path = self._resolve_path(lab_id)
        try:
            result = subprocess.run(
                ["/usr/bin/podman-compose", "-f", str(lab_path / "docker-compose.yml"), "ps"],
                cwd=str(lab_path),
                capture_output=True,
                text=True,
                check=True,
            )

            # Vamos imprimir o output para debug apenas uma vez
            output = result.stdout.lower()

            # Debug visual: se o status der 'unknown', você saberá o porquê
            # print(f"DEBUG OUTPUT: {output}")

            # Lógica mais abrangente
            # Contêineres rodando costumam ter o status 'up' na coluna de estado
            if "up" in output:
                state = LaboratoryState.RUNNING
            # Contêineres criados mas parados costumam exibir 'exited' ou 'created'
            elif "exited" in output or "created" in output or "stopped" in output:
                state = LaboratoryState.STOPPED
            else:
                state = LaboratoryState.UNKNOWN

            return LaboratoryStatus(state=state)
        except subprocess.CalledProcessError as e:
            raise LabExecutionError(f"Erro ao consultar status: {e.stderr.strip()}") from e

    def restart(self, lab_id: str) -> LabExecutionReport:
        """Reinicia a infraestrutura."""
        lab_path = self._resolve_path(lab_id)
        try:
            subprocess.run(
                ["podman-compose", "-f", "docker-compose.yml", "restart"],
                cwd=lab_path,
                capture_output=True,
                text=True,
                check=True,
            )
            return LabExecutionReport(
                lab_id=lab_id, success=True, message="Laboratório reiniciado com sucesso."
            )
        except subprocess.CalledProcessError as e:
            raise LabExecutionError(
                f"Falha ao reiniciar o lab '{lab_id}'.\nErro: {e.stderr.strip()}"
            ) from e

    def logs(self, lab_id: str) -> LabLogs:
        """Coleta logs de execução."""
        lab_path = self._resolve_path(lab_id)
        try:
            result = subprocess.run(
                ["podman-compose", "-f", "docker-compose.yml", "logs"],
                cwd=lab_path,
                capture_output=True,
                text=True,
                check=True,
            )
            return LabLogs(lab_id=lab_id, content=result.stdout)
        except subprocess.CalledProcessError as e:
            raise LabExecutionError(
                f"Falha ao coletar logs do lab '{lab_id}'.\nErro: {e.stderr.strip()}"
            ) from e
