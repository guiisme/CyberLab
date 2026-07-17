import subprocess
from pathlib import Path

from cyberlab.infrastructure.logger import logger
from cyberlab.sdk import LabExecutionReport, LabLifeCycleProtocol, LabLogs


class KubernetesLifecycle(LabLifeCycleProtocol):
    def __init__(self, namespace: str = "lab-pentest"):
        self.namespace = namespace

    def _get_deployment_name(self, lab_id: str) -> str:
        # Padronização: assume que o name no metadata do YAML é o próprio lab_id
        return lab_id

    def run(self, lab_id: str) -> LabExecutionReport:
        from cyberlab.infrastructure.environment import CYBERLAB_HOME

        # 1. Monta o caminho dinâmico para a pasta k8s padrão
        lab_dir = CYBERLAB_HOME / "labs" / lab_id
        manifest_path = lab_dir / "k8s" / "deployment.yaml"

        # 2. Fallback caso o laboratório use infra.yaml diretamente na raiz do lab
        if not manifest_path.exists():
            manifest_path = lab_dir / "infra.yaml"

        if not manifest_path.exists():
            raise FileNotFoundError(
                f"❌ Nenhum manifesto Kubernetes (deployment.yaml ou infra.yaml) "
                f"encontrado para o laboratório '{lab_id}'."
            )

        # 3. Executa o deploy real no cluster
        try:
            subprocess.run(
                ["kubectl", "apply", "-f", str(manifest_path), "-n", self.namespace],
                check=True,
                capture_output=True,
                text=True,
            )
            return LabExecutionReport(lab_id=lab_id, success=True)
        except subprocess.CalledProcessError as e:
            logger.error(f"Falha ao aplicar o manifesto K8s no lab '{lab_id}': {e.stderr}")
            raise  # Mantemos o raise para parar a execução, mas agora com o erro logado!

    def stop(self, lab_id: str) -> None:
        name = self._get_deployment_name(lab_id)
        subprocess.run(
            ["kubectl", "scale", "deployment", name, "--replicas=0", "-n", self.namespace],
            check=True,
        )

    def down(self, lab_id: str) -> None:
        name = self._get_deployment_name(lab_id)
        # Removemos deployment e service relacionados ao lab pelo label no namespace correto
        subprocess.run(["kubectl", "delete", "deployment", name, "-n", self.namespace], check=True)
        subprocess.run(
            ["kubectl", "delete", "svc", "-l", f"app={lab_id}", "-n", self.namespace], check=True
        )

    def status(self, lab_id: str) -> str:
        try:
            # Pegamos a lista de pods filtrada pelo label no namespace correto
            cmd = [
                "kubectl",
                "get",
                "pods",
                "-n",
                self.namespace,
                "-l",
                f"app={lab_id}",
                "-o",
                "name",
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)

            # Se não retornar nomes de pods, o lab não existe ou está parado
            if not result.stdout.strip():
                return "Down"

            # Se encontrou, agora pegamos o status do primeiro da lista
            cmd_status = [
                "kubectl",
                "get",
                "pods",
                "-n",
                self.namespace,
                "-l",
                f"app={lab_id}",
                "-o",
                "jsonpath={.items[0].status.phase}",
            ]
            status_result = subprocess.run(cmd_status, capture_output=True, text=True)

            return status_result.stdout.strip()
        except Exception as e:
            return f"Error: {e}"

    def logs(self, lab_id: str) -> LabLogs:
        try:
            # Refinado para pegar o primeiro pod disponível com segurança
            cmd = [
                "kubectl",
                "get",
                "pod",
                "-n",
                self.namespace,
                "-l",
                f"app={lab_id}",
                "-o",
                "jsonpath={.items[0].metadata.name}",
            ]
            pod_name = subprocess.check_output(cmd, text=True).strip()

            result = subprocess.run(
                ["kubectl", "logs", pod_name, "-n", self.namespace], capture_output=True, text=True
            )
            return LabLogs(content=result.stdout, lab_id=lab_id)
        except subprocess.CalledProcessError as e:
            return LabLogs(content=f"Erro ao obter logs: {e.output}", lab_id=lab_id)

    def proxy(self, lab_id: str) -> None:
        try:
            # Busca o nome do serviço
            cmd_svc = [
                "kubectl",
                "get",
                "svc",
                "-n",
                self.namespace,
                "-l",
                f"app={lab_id}",
                "-o",
                "jsonpath={.items[0].metadata.name}",
            ]
            service_name = subprocess.check_output(cmd_svc, text=True).strip()

            # Busca a porta do serviço automaticamente (porta externa)
            cmd_port = [
                "kubectl",
                "get",
                "svc",
                service_name,
                "-n",
                self.namespace,
                "-o",
                "jsonpath={.spec.ports[0].port}",
            ]
            service_port = subprocess.check_output(cmd_port, text=True).strip()

            print(f"🔗 Conectando ao serviço: {service_name} na porta {service_port}")
            # Mapeia 8080 local para a porta descoberta do serviço
            subprocess.run(
                [
                    "kubectl",
                    "port-forward",
                    "-n",
                    self.namespace,
                    f"svc/{service_name}",
                    f"8080:{service_port}",
                ]
            )
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao iniciar proxy: {e}")

    def restart(self, lab_id: str) -> None:
        # Exemplo de implementação limpa para reiniciar os pods sem baixar o serviço
        name = self._get_deployment_name(lab_id)
        subprocess.run(
            ["kubectl", "rollout", "restart", f"deployment/{name}", "-n", self.namespace],
            check=True,
        )

    def check_requirements(self) -> bool:
        try:
            subprocess.run(["kubectl", "version", "--client"], check=True, capture_output=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def exec(self, lab_id: str, command: str) -> str:
        # Renomeamos localmente para 'target_pod' para manter a legibilidade do código interno
        target_pod = lab_id

        # Se o argumento já contiver o hash dinâmico do pod (
        # termina com o padrão de hash de réplica),
        # use-lo diretamente. Caso contrário, busca pela label.
        if len(target_pod.split("-")[-1]) == 5 and len(target_pod.split("-")) > 2:
            pod_name = target_pod
        else:
            # Busca dinâmica utilizando a label app no namespace correto
            try:
                cmd_pod = [
                    "kubectl",
                    "get",
                    "pod",
                    "-n",
                    self.namespace,
                    "-l",
                    f"app={target_pod}",
                    "-o",
                    "jsonpath={.items[0].metadata.name}",
                ]
                pod_name = subprocess.check_output(cmd_pod, text=True).strip()
            except subprocess.CalledProcessError:
                return f"❌ Erro: Nenhum pod encontrado para a label/nome '{target_pod}'."

        # O "bash -c" executa comandos complexos perfeitamente
        full_cmd = ["kubectl", "exec", "-n", self.namespace, pod_name, "--", "bash", "-c", command]
        result = subprocess.run(full_cmd, capture_output=True, text=True)

        if result.returncode != 0:
            return f"Erro ao executar: {result.stderr}"

        return result.stdout.strip() if result.stdout.strip() else "(comando executado sem saída)"

    def harden(self, lab_id: str) -> str:
        harden_file = f"labs/{lab_id}/hardened-deployment.yaml"
        cmd = ["kubectl", "apply", "-f", harden_file, "-n", self.namespace]
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            return f"❌ Erro ao aplicar hardening: {result.stderr}"

        return "✅ Lab blindado com sucesso via manifesto!"

    def deploy(self, lab_path: str) -> str:
        # Extrai o nome do lab a partir do caminho para o log
        lab_id = Path(lab_path).parts[-2] if "labs" in Path(lab_path).parts else "desconhecido"

        target_path = Path(lab_path)
        # ... (seu código de verificação de caminho)

        try:
            subprocess.run(
                ["kubectl", "apply", "-f", str(target_path)], check=True, capture_output=True
            )

            # Ajustado para usar lab_id definido acima
            logger.info(f"Manifesto K8s aplicado com sucesso para o lab '{lab_id}'.")

            return "✅ Laboratório implantado com sucesso! "
            f"Verifique os pods com 'kubectl get pods -n {self.namespace}'"
        except subprocess.CalledProcessError as e:
            # Também seria uma boa prática logar o erro aqui, como fizemos no método run()
            logger.error(f"Falha na implantação do lab '{lab_id}': {e.stderr.decode()}")
            return f"❌ Erro na implantação: {e.stderr.decode()}"

    def setup_ctf(self, lab_id: str, target_pod: str) -> str:
        # A string do script não precisa encapsular "bash -c" aqui, pois o self.exec já
        # faz isso por baixo do capô!
        script = "mkdir -p /tmp/ctf && echo 'FLAG_1_RECON_COMPLETE' > /tmp/ctf/dica.txt"
        return self.exec(target_pod, script)
