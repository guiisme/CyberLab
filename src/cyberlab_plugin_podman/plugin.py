from typing import Any

from cyberlab.sdk import Plugin, PluginManifest
from cyberlab_plugin_podman.infrastructure.podman_compose import PodmanComposeLabLifecycle


class PodmanPlugin(Plugin):
    """
    Plugin oficial do CyberLab para execução de laboratórios via Podman.
    """

    def __init__(self, **kwargs: Any) -> None:
        # 1. Instanciamos o manifesto estrito
        manifest = PluginManifest(
            id="podman",
            name="Podman Execution Adapter",
            version="0.1.0",
            description="Adds support for running laboratories using podman-compose",
            author="CyberLab",
            capabilities=("lab_lifecycle",),
        )

        # 2. Entregamos o manifesto para a inicialização da classe base (Plugin)
        super().__init__(manifest=manifest, **kwargs)

    def get_lifecycle_adapter(self) -> PodmanComposeLabLifecycle:
        """Instancia e retorna o adaptador de infraestrutura sob demanda."""
        return PodmanComposeLabLifecycle()
