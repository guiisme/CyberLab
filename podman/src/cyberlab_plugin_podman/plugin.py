from cyberlab.sdk import PluginManifest
from podman.src.cyberlab_plugin_podman.infrastructure.podman_compose import (
    PodmanComposeLabLifecycle,
)


class Podman:
    (
        """Example CyberLab plugin."""
        """
    Classe principal do plugin que o Core do CyberLab carrega dinamicamente.
    """
    )

    def __init__(self) -> None:
        # Instanciamos o adaptador de infraestrutura de forma isolada
        self._lifecycle = PodmanComposeLabLifecycle()

    @property
    def manifest(self) -> PluginManifest:
        return PluginManifest(
            id="podman",
            name="Podman",
            version="0.1.0",
            description="Adds support for running laboratories using podman-compose",
            author="Guiisme84",
            capabilities=(),
        )

    def get_lifecycle_adapter(self) -> PodmanComposeLabLifecycle:
        """
        Método que expõe o adaptador para o Core (através do SDK).
        """
        return self._lifecycle
