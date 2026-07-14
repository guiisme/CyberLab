from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PluginManifest:
    """Metadata describing a CyberLab plugin."""

    id: str
    name: str
    version: str
    description: str
    author: str
    capabilities: tuple[str, ...]
