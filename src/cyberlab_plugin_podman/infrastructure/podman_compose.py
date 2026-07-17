import json
import shutil
import subprocess
from pathlib import Path

from cyberlab.sdk import (
    LabExecutionError,
    LabExecutionReport,
    LabLifeCycleProtocol,
    LabLogs,
)


class PodmanComposeLabLifecycle(LabLifeCycleProtocol):
    """Infrastructure adapter that manages laboratories with podman-compose."""

    def _resolve_path(self, lab_id: str) -> Path:
        return (Path.cwd() / lab_id).resolve()

    def _execute(self, lab_id: str, *operation: str) -> subprocess.CompletedProcess[str]:
        lab_path = self._resolve_path(lab_id)
        command = ["podman-compose", "-f", str(lab_path / "docker-compose.yml"), *operation]

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
            raise LabExecutionError(
                f"Podman Compose {' '.join(operation)} failed: {details.strip()}"
            ) from error

    def run(self, lab_id: str) -> LabExecutionReport:
        # ... (seu código de subprocesso aqui) ...

        # Ajuste para preencher os argumentos obrigatórios:
        return LabExecutionReport(
            lab_id=lab_id,
            success=True,
            message="Lab subiu com sucesso!",  # Se você tiver um campo message
        )

    def stop(self, lab_id: str) -> None:
        subprocess.run(
            ["podman-compose", "-f", f"labs/{lab_id}/podman-compose.yml", "stop"], check=True
        )

    def down(self, lab_id: str) -> None:
        subprocess.run(
            ["podman-compose", "-f", f"labs/{lab_id}/podman-compose.yml", "down"], check=True
        )

    def status(self, lab_id: str) -> str:
        # Verifica se existem containers rodando para este lab
        result = subprocess.run(
            ["podman-compose", "-f", f"labs/{lab_id}/podman-compose.yml", "ps"],
            capture_output=True,
            text=True,
        )
        if "Up" in result.stdout:
            return "running"
        return "stopped"

    def restart(self, lab_id: str) -> None:
        print(f"🔄 Reiniciando containers do lab: {lab_id}...")
        # O podman-compose facilita muito: ele sobe/desce baseado no arquivo
        subprocess.run(
            ["podman-compose", "-f", f"labs/{lab_id}/podman/podman-compose.yml", "down"], check=True
        )
        subprocess.run(
            ["podman-compose", "-f", f"labs/{lab_id}/podman/podman-compose.yml", "up", "-d"],
            check=True,
        )

    def check_requirements(self) -> bool:
        # Verifica se podman-compose ou docker-compose estão no PATH
        return (
            shutil.which("podman-compose") is not None or shutil.which("docker-compose") is not None
        )

    def logs(self, lab_id: str) -> LabLogs:
        result = subprocess.run(
            ["podman-compose", "-f", f"labs/{lab_id}/podman-compose.yml", "logs"],
            capture_output=True,
            text=True,
        )
        # Retorna o objeto esperado pelo protocolo
        return LabLogs(content=result.stdout, lab_id=lab_id)

    def check(self, lab_id: str) -> None:
        print(f"🔍 Executando auditoria no ambiente Podman: {lab_id}...")

        # 1. Checagem: O container está rodando como Root?
        # O comando 'inspect' do podman nos dá o JSON completo da configuração
        cmd_inspect = ["podman", "inspect", f"{lab_id}-web-vulneravel"]
        result = subprocess.run(cmd_inspect, capture_output=True, text=True)
        data = json.loads(result.stdout)

        user = data[0]["Config"]["User"]
        if user == "" or user == "root":
            print("⚠️ [ALERTA]: Container rodando como root!")
        else:
            print(f"✅ [OK]: Container rodando com usuário: {user}")

        # 2. Checagem: O container tem privilégios excessivos?
        cap = data[0]["HostConfig"]["CapAdd"]
        if cap:
            print(f"⚠️ [ALERTA]: O container possui capacidades adicionais: {cap}")
        else:
            print("✅ [OK]: Nenhuma capacidade de privilégio adicional encontrada.")

    def deploy(self, lab_path: str) -> str:
        """Executa a implantação do lab."""
        import subprocess

        try:
            result = subprocess.run(
                ["kubectl", "apply", "-f", lab_path], check=True, capture_output=True, text=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            raise Exception(f"Erro no deploy: {e.stderr}") from e

    def setup_ctf(self, lab_id: str, target_pod: str = "default_target") -> str:
        # Script que cria as flags no container alvo (exemplo)
        # Ajuste o nome do container se necessário
        setup_script = """
        echo "FLAG_1_RECON_COMPLETE" > /var/www/html/dica.txt
        echo "Olá, Well! A senha do cofre é 123456" > /var/www/html/email_secreto.txt
        """
        # Usamos o método exec que você já criou para injetar o setup
        return self.exec(lab_id, f"bash -c '{setup_script}'")

    def exec(self, lab_id: str, command: str) -> str:
        """Executa um comando dentro de um lab."""
        # Se for Podman, aqui vai sua lógica de subprocesso
        # Se for K8s, aqui vai o 'kubectl exec'
        import subprocess

        # Exemplo simplificado:
        result = subprocess.run(
            ["kubectl", "exec", lab_id, "--", "/bin/sh", "-c", command],
            capture_output=True,
            text=True,
        )
        return result.stdout
