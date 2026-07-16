import subprocess
from pathlib import Path

from cyberlab.sdk import (
    LabExecutionReport,
    LabLifeCycleProtocol,
    LabLogs,
)
from cyberlab.utils.network import start_port_forward


class KubernetesLifecycle(LabLifeCycleProtocol):
    def _resolve_path(self, lab_id: str) -> Path:
        # Assumindo a mesma lógica de resolução de caminho que você já tem
        return Path.cwd() / lab_id

    def _verify_root_access(self, lab_id: str) -> bool:
        # Mudamos o jsonpath para olhar para spec.securityContext (nível do Pod)
        cmd = [
            "kubectl",
            "get",
            "pod",
            "-l",
            f"app={lab_id}",
            "-o",
            "jsonpath={.items[0].spec.securityContext.runAsNonRoot}",
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)

        # O valor correto é "true". Se não for, está vulnerável.
        return result.stdout.strip() != "true"

    def run(self, lab_id: str) -> LabExecutionReport:
        # 1. Defina o caminho do manifesto (mantendo o padrão /labs/)
        manifest_path = Path.cwd() / "labs" / lab_id / "k8s" / "deployment.yaml"

        # 2. Comando para aplicar o manifesto
        subprocess.run(["kubectl", "apply", "-f", str(manifest_path)], check=True)

        # 3. Retorne o objeto corretamente preenchido
        return LabExecutionReport(lab_id=lab_id, success=True)

    def stop(self, lab_id: str) -> None:
        # Escala o deployment para 0 para parar os pods
        subprocess.run(["kubectl", "scale", "deployment", lab_id, "--replicas=0"], check=True)

    def down(self, lab_id: str) -> None:
        # Remove todo o recurso
        subprocess.run(["kubectl", "delete", "deployment", lab_id], check=True)

    def status(self, lab_id: str) -> str:
        """Consulta o status real do Pod no Kubernetes."""
        # O comando abaixo retorna a fase do pod (Running, Pending, Failed, etc)
        cmd = [
            "kubectl",
            "get",
            "pod",
            "-l",
            f"app={lab_id}",
            "-o",
            "jsonpath={.items[0].status.phase}",
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return result.stdout.strip() if result.stdout.strip() else "NOT_FOUND"
        except subprocess.CalledProcessError:
            return "NOT_FOUND"

    def logs(self, lab_id: str) -> LabLogs:
        # Busca o nome do primeiro pod que tenha o label app=lab_id
        cmd_pod = [
            "kubectl",
            "get",
            "pod",
            "-l",
            f"app={lab_id}",
            "-o",
            "jsonpath={.items[0].metadata.name}",
        ]
        pod_name = subprocess.check_output(cmd_pod, text=True).strip()

        # Agora busca os logs desse pod específico
        cmd_logs = ["kubectl", "logs", pod_name]
        result = subprocess.run(cmd_logs, capture_output=True, text=True)

        return LabLogs(content=result.stdout, lab_id=lab_id)

    def restart(self, lab_id: str) -> None:
        print(f"🔄 Reiniciando deployment do lab: {lab_id}...")
        subprocess.run(["kubectl", "rollout", "restart", f"deployment/{lab_id}"], check=True)
        # Retorna None, mantendo a assinatura limpa

    def check_requirements(self) -> bool:
        raise NotImplementedError

    def proxy(self, lab_id: str) -> None:
        """Mantém o port-forward aberto para o laboratório."""
        print(f"🔗 Iniciando túnel de rede para o lab: {lab_id}...")
        try:
            # O start_port_forward retorna o objeto Popen
            process = start_port_forward(lab_id)
            print("✅ Proxy ativo. Acesse http://localhost:8080")
            print("🛑 Pressione Ctrl+C para encerrar o proxy.")

            # Bloqueia a execução aqui mantendo o túnel aberto
            process.wait()

        except KeyboardInterrupt:
            print("\n🛑 Encerrando túnel...")
            if process:  # type: ignore
                process.terminate()

    # No seu adaptador
    def check(self, lab_id: str) -> None:
        print(f"🔍 Auditoria de Segurança: {lab_id}")

        # Exemplo de lógica de verificação
        is_root = self._verify_root_access(lab_id)

        if is_root:
            print(
                "❌ [CRÍTICO]: O container está rodando como ROOT. "
                "Vulnerabilidade de escalação de privilégios!"
            )
        else:
            print("✅ [OK]: Container rodando com usuário restrito.")
