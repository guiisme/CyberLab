import subprocess
from pathlib import Path

from cyberlab.sdk import LabLifecycleProtocol


class PodmanComposeLabLifecycle(LabLifecycleProtocol):
    """
    Implementação do ciclo de vida de laboratórios utilizando podman-compose.
    Atua como um adaptador de infraestrutura na Hexagonal Architecture.
    """

    def run(self, lab_path: Path) -> None:
        """Inicializa o ambiente do laboratório em background."""
        subprocess.run(["podman-compose", "up", "-d"], cwd=lab_path, check=True)

    def stop(self, lab_path: Path) -> None:
        """Para e remove os containers e redes do laboratório."""
        subprocess.run(["podman-compose", "down"], cwd=lab_path, check=True)

    def status(self, lab_path: Path) -> str:
        """Retorna o status dos containers do laboratório."""
        result = subprocess.run(
            ["podman-compose", "ps"], cwd=lab_path, capture_output=True, text=True, check=True
        )
        return result.stdout

    def restart(self, lab_path: Path) -> None:
        """Reinicia os containers e redes do laboratório."""
        subprocess.run(["podman-compose", "restart"], cwd=lab_path, check=True)

    def logs(self, lab_path: Path, follow: bool = False, tail: bool = False) -> None:
        """Exibe os logs do laboratório com suporte a follow e tail."""
        command = ["podman-compose", "logs"]

        if follow:
            command.append("--follow")
        if tail:
            # Emulando o comportamento padrão de tail do compose
            command.append("--tail=all")

        subprocess.run(command, cwd=lab_path, check=True)
