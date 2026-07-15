from cyberlab.sdk import Plugin, PluginManifest
from cyberlab_plugin_docker_adapter.infrastructure.adapter import (
    DockerAdapterPluginLifecycleAdapter,
)


class DockerAdapterPlugin(Plugin):
    """
    Um novo plugin para o CyberLab
    """

    def __init__(self, **kwargs) -> None:
        manifest = PluginManifest(
            id="docker-adapter",
            name="Docker Adapter",
            version="0.1.0",
            description="Um novo plugin para o CyberLab",
            author="Gui",
            # Declaramos a capacidade para o Core saber o que este plugin faz
            capabilities=("lab_lifecycle",),
        )
        super().__init__(manifest=manifest, **kwargs)

    def get_lifecycle_adapter(self) -> DockerAdapterPluginLifecycleAdapter:
        """Instancia e retorna o adaptador de infraestrutura sob demanda."""
        return DockerAdapterPluginLifecycleAdapter()
