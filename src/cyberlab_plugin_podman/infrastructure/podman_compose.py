import json
import shutil
import subprocess
from pathlib import Path

from cyberlab.domain.models.lab_execution_report import LaboratoryState, LaboratoryStatus
from cyberlab.infrastructure.logger import logger
from cyberlab.sdk import (
    LabExecutionError,
    LabExecutionReport,
    LabLifeCycleProtocol,
    LabLogs,
)


class PodmanComposeLabLifecycle(LabLifeCycleProtocol):
    """Infrastructure adapter that manages laboratories with podman-compose."""

    _PODMAN_COMPOSE = "/usr/bin/podman-compose"

    def _resolve_path(self, lab_id: str) -> Path:
        return (Path.cwd() / lab_id).resolve()

    def _execute(self, lab_id: str, *operation: str) -> subprocess.CompletedProcess[str]:
        lab_path = self._resolve_path(lab_id)
        command = [self._PODMAN_COMPOSE, "-f", str(lab_path / "docker-compose.yml"), *operation]

        try:
            return subprocess.run(
                command,
                cwd=lab_path,
                capture_output=True,
                text=True,
                check=True,
            )
        except subprocess.CalledProcessError as error:
            details = error.stderr or error.stdout or str(error)
            raise LabExecutionError(f"Erro no Podman: {details.strip()}") from error

    def run(self, lab_id: str) -> LabExecutionReport:
        self._execute(lab_id, "up", "-d")
        return LabExecutionReport(
            lab_id=lab_id,
            success=True,
            message="Lab subiu com sucesso!",
        )

    def stop(self, lab_id: str) -> LabExecutionReport:
        self._execute(lab_id, "stop")
        return LabExecutionReport(
            lab_id=lab_id,
            success=True,
            message="Lab parado com sucesso!",
        )

    def down(self, lab_id: str) -> None:
        subprocess.run(
            ["podman-compose", "-f", f"labs/{lab_id}/podman-compose.yml", "down"], check=True
        )

    def status(self, lab_id: str) -> LaboratoryStatus:
        result = self._execute(lab_id, "ps")
        if "Up" in result.stdout:
            return LaboratoryStatus(LaboratoryState.RUNNING)
        return LaboratoryStatus(LaboratoryState.STOPPED)

    def restart(self, lab_id: str) -> LabExecutionReport:
        logger.info(f"🔄 Reiniciando containers do lab: {lab_id}...")
        self._execute(lab_id, "restart")
        return LabExecutionReport(
            lab_id=lab_id,
            success=True,
            message="Lab reiniciado com sucesso!",
        )

    def check_requirements(self) -> bool:
        # Verifica se podman-compose ou docker-compose estão no PATH
        return (
            shutil.which("podman-compose") is not None or shutil.which("docker-compose") is not None
        )

    def logs(self, lab_id: str) -> LabLogs:
        result = self._execute(lab_id, "logs")
        return LabLogs(content=result.stdout, lab_id=lab_id)

    def check(self, lab_id: str) -> None:
        logger.info(f"🔍 Executando auditoria no ambiente Podman: {lab_id}...")

        # 1. Checagem: O container está rodando como Root?
        # O comando 'inspect' do podman nos dá o JSON completo da configuração
        cmd_inspect = ["podman", "inspect", f"{lab_id}-web-vulneravel"]
        result = subprocess.run(cmd_inspect, capture_output=True, text=True)
        data = json.loads(result.stdout)

        user = data[0]["Config"]["User"]
        if user == "" or user == "root":
            logger.warning("⚠️ [ALERTA]: Container rodando como root!")
        else:
            logger.warning(f"✅ [OK]: Container rodando com usuário: {user}")

        # 2. Checagem: O container tem privilégios excessivos?
        cap = data[0]["HostConfig"]["CapAdd"]
        if cap:
            logger.warning(f"⚠️ [ALERTA]: O container possui capacidades adicionais: {cap}")
        else:
            logger.info("✅ [OK]: Nenhuma capacidade de privilégio adicional encontrada.")

    def deploy(self, lab_path: str) -> str:
        """Start the Podman Compose laboratory declared by a manifest path."""

        lab_id = Path(lab_path).parent.name
        return self.run(lab_id).message

    def setup_ctf(self, lab_id: str, target_pod: str = "default_target") -> str:
        # Script que cria as flags no container alvo (exemplo)
        # Ajuste o nome do container se necessário
        setup_script = """
        echo "FLAG_1_RECON_COMPLETE" > /var/www/html/dica.txt
        echo "Olá, Well! A senha do cofre é 123456" > /var/www/html/email_secreto.txt"""
        return self.exec(lab_id, f"bash -c '{setup_script}'")

    def exec(self, lab_id: str, command: str) -> str:
        """Execute a non-interactive command in the laboratory container."""

        containers = subprocess.run(
            ["podman", "ps", "--filter", f"name={lab_id}", "--format", "{{.Names}}"],
            capture_output=True,
            text=True,
        )
        container_names = containers.stdout.splitlines()
        if not container_names:
            return f"Erro ao executar: nenhum container encontrado para '{lab_id}'."

        result = subprocess.run(
            ["podman", "exec", container_names[0], "sh", "-c", command],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            return f"Erro ao executar: {result.stderr.strip()}"
        return result.stdout.strip() or "(comando executado sem saída)"

    def exec_in_pod(self, lab_id: str, command: str = "/bin/bash"):
        """Acessa um shell interativo dentro do container do Podman Compose."""
        try:
            import subprocess

            # No Podman Compose, o nome do container geralmente
            # segue o padrão: {lab_id}_{serviço}_1
            # Como convenção do seu framework, podemos buscar o
            # container que tenha o nome do lab_id.
            # Uma forma segura é listar os containers ativos
            # filtrando pelo nome do lab:
            cmd_find_container = [
                "podman",
                "ps",
                "--filter",
                f"name={lab_id}",
                "--format",
                "{{.Names}}",
            ]

            output = subprocess.check_output(cmd_find_container, text=True).strip()
            containers = output.splitlines()

            if not containers:
                logger.error(f"❌ Erro: Nenhum container encontrado para o laboratório '{lab_id}'.")
                return

            # Seleciona o primeiro container encontrado para o lab
            container_name = containers[0]

            # Executa o comando de forma interativa no terminal
            # Passamos dentro de 'bash -c' para manter o mesmo comportamento robusto do K8s
            full_cmd = ["podman", "exec", "-it", container_name, "bash", "-c", command]
            subprocess.run(full_cmd)

        except Exception as e:
            logger.error(f"❌ Erro ao conectar ao container Podman do lab '{lab_id}': {e}")
