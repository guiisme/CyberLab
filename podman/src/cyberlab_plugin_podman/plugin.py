from cyberlab.sdk import PluginManifest


class Podman:
    """Example CyberLab plugin."""

    @property
    def manifest(self) -> PluginManifest:
        return PluginManifest(
            id="podman",
            name="Podman",
            version="0.1.0",
            description="Example CyberLab plugin.",
            author="CyberLab",
            capabilities=(),
        )
