import subprocess
from pathlib import Path

from cyberlab.infrastructure.logger import logger
from cyberlab.sdk import LabExecutionReport, LabLifeCycleProtocol, LabLogs


class KubernetesLifecycle(LabLifeCycleProtocol):
    def __init__(self):
        # Namespace agora é gerenciado dinamicamente por lab_id em cada método
        pass

    def _get_deployment_name(self, lab_id: str) -> str:
        return lab_id

    def _ensure_namespace(self, lab_id: str):
        # Cria o namespace se não existir de forma segura
        subprocess.run(
            ["kubectl", "create", "namespace", lab_id, "--dry-run=client", "-o", "yaml"],
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["kubectl", "apply", "-f", "-"],
            input=f"apiVersion: v1\nkind: Namespace\nmetadata:\n  name: {lab_id}",
            text=True,
            check=True,
        )

    def run(self, lab_id: str) -> LabExecutionReport:
        from cyberlab.infrastructure.environment import CYBERLAB_HOME

        lab_dir = CYBERLAB_HOME / "labs" / lab_id
        manifest_path = lab_dir / "k8s" / "deployment.yaml"

        if not manifest_path.exists():
            manifest_path = lab_dir / "infra.yaml"

        if not manifest_path.exists():
            raise FileNotFoundError(f"❌ Nenhum manifesto Kubernetes encontrado para '{lab_id}'.")

        try:
            self._ensure_namespace(lab_id)
            subprocess.run(
                ["kubectl", "apply", "-f", str(manifest_path), "-n", lab_id],
                check=True,
                capture_output=True,
                text=True,
            )
            return LabExecutionReport(lab_id=lab_id, success=True)
        except subprocess.CalledProcessError as e:
            logger.error(f"Falha ao aplicar manifesto em '{lab_id}': {e.stderr}")
            raise

    def stop(self, lab_id: str) -> None:
        name = self._get_deployment_name(lab_id)
        subprocess.run(
            ["kubectl", "scale", "deployment", name, "--replicas=0", "-n", lab_id],
            check=True,
        )

    def down(self, lab_id: str) -> None:
        logger.info(f"Removendo infraestrutura do lab '{lab_id}' via namespace.")
        subprocess.run(
            ["kubectl", "delete", "namespace", lab_id, "--ignore-not-found=true"], check=True
        )

    def status(self, lab_id: str) -> str:
        try:
            cmd = ["kubectl", "get", "pods", "-n", lab_id, "-l", f"app={lab_id}", "-o", "name"]
            result = subprocess.run(cmd, capture_output=True, text=True)

            if not result.stdout.strip():
                return "Down"

            cmd_status = [
                "kubectl",
                "get",
                "pods",
                "-n",
                lab_id,
                "-l",
                f"app={lab_id}",
                "-o",
                "jsonpath={.items[0].status.phase}",
            ]
            return subprocess.run(cmd_status, capture_output=True, text=True).stdout.strip()
        except Exception as e:
            return f"Error: {e}"

    def logs(self, lab_id: str) -> LabLogs:
        try:
            cmd = [
                "kubectl",
                "get",
                "pod",
                "-n",
                lab_id,
                "-l",
                f"app={lab_id}",
                "-o",
                "jsonpath={.items[0].metadata.name}",
            ]
            pod_name = subprocess.check_output(cmd, text=True).strip()
            result = subprocess.run(
                ["kubectl", "logs", pod_name, "-n", lab_id], capture_output=True, text=True
            )
            return LabLogs(content=result.stdout, lab_id=lab_id)
        except subprocess.CalledProcessError as e:
            return LabLogs(content=f"Erro ao obter logs: {e.output}", lab_id=lab_id)

    def proxy(self, lab_id: str) -> None:
        try:
            cmd_svc = [
                "kubectl",
                "get",
                "svc",
                "-n",
                lab_id,
                "-l",
                f"app={lab_id}",
                "-o",
                "jsonpath={.items[0].metadata.name}",
            ]
            service_name = subprocess.check_output(cmd_svc, text=True).strip()
            cmd_port = [
                "kubectl",
                "get",
                "svc",
                service_name,
                "-n",
                lab_id,
                "-o",
                "jsonpath={.spec.ports[0].port}",
            ]
            service_port = subprocess.check_output(cmd_port, text=True).strip()

            print(f"🔗 Conectando ao serviço: {service_name} na porta {service_port}")
            subprocess.run(
                [
                    "kubectl",
                    "port-forward",
                    "-n",
                    lab_id,
                    f"svc/{service_name}",
                    f"8080:{service_port}",
                ]
            )
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao iniciar proxy: {e}")

    def restart(self, lab_id: str) -> None:
        name = self._get_deployment_name(lab_id)
        subprocess.run(
            ["kubectl", "rollout", "restart", f"deployment/{name}", "-n", lab_id], check=True
        )

    def check_requirements(self) -> bool:
        try:
            subprocess.run(["kubectl", "version", "--client"], check=True, capture_output=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def exec(self, lab_id: str, command: str) -> str:
        target_pod = lab_id
        if len(target_pod.split("-")[-1]) == 5 and len(target_pod.split("-")) > 2:
            pod_name = target_pod
        else:
            try:
                cmd_pod = [
                    "kubectl",
                    "get",
                    "pod",
                    "-n",
                    lab_id,
                    "-l",
                    f"app={target_pod}",
                    "-o",
                    "jsonpath={.items[0].metadata.name}",
                ]
                pod_name = subprocess.check_output(cmd_pod, text=True).strip()
            except subprocess.CalledProcessError:
                return f"❌ Erro: Nenhum pod encontrado para '{target_pod}'."

        full_cmd = ["kubectl", "exec", "-n", lab_id, pod_name, "--", "bash", "-c", command]
        result = subprocess.run(full_cmd, capture_output=True, text=True)
        return (
            result.stdout.strip()
            if result.returncode == 0
            else f"Erro ao executar: {result.stderr}"
        )

    def harden(self, lab_id: str) -> str:
        harden_file = f"labs/{lab_id}/hardened-deployment.yaml"
        result = subprocess.run(
            ["kubectl", "apply", "-f", harden_file, "-n", lab_id], capture_output=True, text=True
        )
        return (
            "✅ Lab blindado com sucesso!"
            if result.returncode == 0
            else f"❌ Erro: {result.stderr}"
        )

    def deploy(self, lab_path: str) -> str:
        lab_id = Path(lab_path).parts[-2] if "labs" in Path(lab_path).parts else "desconhecido"
        target_path = Path(lab_path)

        try:
            self._ensure_namespace(lab_id)
            subprocess.run(
                ["kubectl", "apply", "-f", str(target_path), "-n", lab_id],
                check=True,
                capture_output=True,
            )
            logger.info(f"Manifesto K8s aplicado com sucesso para o lab '{lab_id}'.")
            return f"✅ Laboratório '{lab_id}' implantado com sucesso!"
        except subprocess.CalledProcessError as e:
            logger.error(f"Falha na implantação do lab '{lab_id}': {e.stderr.decode()}")
            return f"❌ Erro na implantação: {e.stderr.decode()}"

    def setup_ctf(self, lab_id: str, target_pod: str) -> str:
        script = "mkdir -p /tmp/ctf && echo 'FLAG_1_RECON_COMPLETE' > /tmp/ctf/dica.txt"
        return self.exec(target_pod, script)
