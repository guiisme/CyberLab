import base64
import subprocess
from pathlib import Path

import yaml

from cyberlab.infrastructure.logger import logger
from cyberlab.sdk import LabExecutionReport, LabLifeCycleProtocol, LabLogs


class KubernetesLifecycle(LabLifeCycleProtocol):
    def __init__(self, lab_id: str):
        # Agora o namespace é dinâmico, baseado no ID do laboratório
        self.namespace = lab_id
        self.lab_id = lab_id

    def _get_deployment_name(self, lab_id: str) -> str:
        # Padronização: assume que o name no metadata do YAML é o próprio lab_id
        return lab_id

    def _ensure_namespace(self, lab_id: str):
        # Cria o namespace diretamente sem o --dry-run
        try:
            subprocess.run(
                ["kubectl", "create", "namespace", lab_id], check=True, capture_output=True
            )
            logger.info(f"Namespace '{lab_id}' criado com sucesso.")
        except subprocess.CalledProcessError as e:
            # Se o erro for "AlreadyExists", ignoramos e seguimos
            if "AlreadyExists" not in e.stderr.decode():
                raise e

    def _ensure_flag_secret(self, lab_id: str, flag_value: str):
        encoded_flag = base64.b64encode(flag_value.encode("utf-8")).decode("utf-8")
        # O uso de textwrap.dedent é recomendado, ou simplesmente alinhe na margem:
        secret_manifest = f"""apiVersion: v1
kind: Secret
metadata:
  name: {lab_id}-flag
  namespace: {lab_id}
type: Opaque
data:
  flag: {encoded_flag}
"""
        subprocess.run(
            ["kubectl", "apply", "-f", "-"], input=secret_manifest, text=True, check=True
        )

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

            logger.info(f"🔗 Conectando ao serviço: {service_name} na porta {service_port}")
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
            logger.error(f"❌ Erro ao iniciar proxy: {e}")

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

    def _validate_lab_structure(self, lab_id: str):
        from cyberlab.infrastructure.environment import CYBERLAB_HOME

        lab_dir = CYBERLAB_HOME / "labs" / lab_id

        required_files = [lab_dir / "lab.yaml", lab_dir / "k8s" / "deployment.yaml"]

        for file_path in required_files:
            if not file_path.exists():
                raise FileNotFoundError(f"❌ Componente obrigatório faltando: {file_path.name}")

        with open(lab_dir / "lab.yaml") as f:
            data = yaml.safe_load(f)
            if not data or "flag" not in data:
                raise ValueError(
                    "❌ O arquivo 'lab.yaml' está incompleto ou sem a 'flag' definida."
                )

    def get_flag_from_cluster(self, lab_id: str) -> str:
        """Busca a flag real diretamente do Secret no cluster."""
        try:
            # Comando para ler o secret no formato base64
            cmd = [
                "kubectl",
                "get",
                "secret",
                f"{lab_id}-flag",
                "-n",
                lab_id,
                "-o",
                "jsonpath={.data.flag}",
            ]
            encoded_flag = subprocess.check_output(cmd, text=True)
            # Decodifica de base64 para texto claro
            return base64.b64decode(encoded_flag).decode("utf-8")
        except Exception as e:
            logger.error(f"Erro ao recuperar flag do cluster: {e}")
            return ""

    def deploy(self, lab_path: str) -> str:
        # lab_path aqui recebe o caminho do lab.yaml, precisamos do caminho do manifesto
        lab_id = self.lab_id

        # Executa a validação antes de qualquer operação no cluster
        try:
            self._validate_lab_structure(lab_id)
        except (FileNotFoundError, ValueError) as e:
            return str(e)

        lab_dir = Path(lab_path).parent
        manifest_path = lab_dir / "k8s" / "deployment.yaml"  # Caminho fixo para o manifesto correto

        # Lê o lab.yaml para a flag
        with open(lab_path) as f:
            lab_data = yaml.safe_load(f)
            flag = lab_data.get("flag", "default-flag")

        try:
            self._ensure_namespace(lab_id)
            self._ensure_flag_secret(lab_id, flag)

            # Aplica o deployment.yaml, NÃO o lab.yaml
            subprocess.run(
                ["kubectl", "apply", "-f", str(manifest_path), "-n", lab_id],
                check=True,
                capture_output=True,
                text=True,
            )
            logger.info(f"Manifesto e Secret da flag aplicados para o lab '{lab_id}'.")
            return f"✅ Laboratório '{lab_id}' implantado com segurança!"
        except subprocess.CalledProcessError as e:
            # O erro detalhado ajudará a ver se o deployment.yaml está correto
            err_msg = e.stderr if hasattr(e, "stderr") else str(e)
            return f"❌ Erro na implantação: {err_msg}"

    def setup_ctf(self, lab_id: str, target_pod: str) -> str:
        # A string do script não precisa encapsular "bash -c" aqui, pois o self.exec já
        # faz isso por baixo do capô!
        script = "mkdir -p /tmp/ctf && echo 'FLAG_1_RECON_COMPLETE' > /tmp/ctf/dica.txt"
        return self.exec(target_pod, script)

    def validate_flag(self, lab_id: str, user_flag: str) -> bool:
        try:
            # Recupera o secret do cluster no namespace do lab
            cmd = [
                "kubectl",
                "get",
                "secret",
                f"{lab_id}-flag",
                "-n",
                lab_id,
                "-o",
                "jsonpath={.data.flag}",
            ]
            encoded_flag = subprocess.check_output(cmd, text=True).strip()

            # Decodifica o valor (Base64) para comparar
            import base64

            actual_flag = base64.b64decode(encoded_flag).decode("utf-8")

            return user_flag == actual_flag
        except subprocess.CalledProcessError:
            logger.error(f"Erro ao buscar flag do laboratório '{lab_id}'.")
            return False

    def exec_in_pod(self, lab_id: str, command: str = "/bin/bash"):
        """Acessa um shell interativo dentro do pod do laboratório."""
        try:
            # 1. Encontra o nome do pod automaticamente
            cmd_find_pod = [
                "kubectl",
                "get",
                "pods",
                "-n",
                lab_id,
                "-l",
                f"app={lab_id}",
                "-o",
                "jsonpath={.items[0].metadata.name}",
            ]
            pod_name = subprocess.check_output(cmd_find_pod, text=True).strip()

            # 2. Executa o comando via kubectl exec de forma interativa
            # Passamos o comando dentro de 'bash -c' para suportar strings complexas sem quebrar
            full_cmd = [
                "kubectl",
                "exec",
                "-it",
                pod_name,
                "-n",
                lab_id,
                "--",
                "bash",
                "-c",
                command,
            ]

            subprocess.run(full_cmd)

        except subprocess.CalledProcessError:
            logger.error(f"❌ Erro: Nenhum pod encontrado para o laboratório '{lab_id}'.")
        except Exception as e:
            logger.error(f"❌ Erro ao conectar ao lab '{lab_id}': {e}")
