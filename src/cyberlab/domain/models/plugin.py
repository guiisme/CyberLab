from dataclasses import dataclass

from cyberlab.domain.models.plugin_manifest import PluginManifest


@dataclass(frozen=True, slots=True)
class Plugin:
    """Represents a CyberLab plugin."""

    manifest: PluginManifest
