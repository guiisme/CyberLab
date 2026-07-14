from cyberlab.sdk import PluginManifest


class HelloPlugin:
    """Example CyberLab plugin."""

    @property
    def manifest(self) -> PluginManifest:
        return PluginManifest(
            id="hello-plugin",
            name="Hello Plugin",
            version="0.1.0",
            description="Example CyberLab plugin.",
            author="CyberLab",
            capabilities=(),
        )
