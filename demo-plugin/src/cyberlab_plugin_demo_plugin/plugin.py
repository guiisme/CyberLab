from cyberlab.sdk import PluginManifest


class DemoPlugin:
    """Example CyberLab plugin."""

    @property
    def manifest(self) -> PluginManifest:
        return PluginManifest(
            id="demo-plugin",
            name="Demo Plugin",
            version="0.1.0",
            description="Example CyberLab plugin.",
            author="CyberLab",
            capabilities=(),
        )
