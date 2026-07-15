from cyberlab.application.interfaces.plugin_protocol import PluginProtocol
from cyberlab.domain.models.plugin_manifest import PluginManifest


class FakePlugin(PluginProtocol):
    name: str  # Silences Pylance

    def __init__(self, plugin_id: str = "fake-plugin", name: str = "my_fake_plugin") -> None:
        self.name = name  # <-- Add this to make it exist at runtime!
        self._manifest = PluginManifest(
            id=plugin_id,
            name="Fake Plugin",
            version="1.0.0",
            description="Fake plugin used for tests.",
            author="CyberLab",
            capabilities=(),
        )

    @property
    def manifest(self) -> PluginManifest:
        return self._manifest
