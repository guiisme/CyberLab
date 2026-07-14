from __future__ import annotations

from typing import Protocol

from cyberlab.domain.models.plugin_manifest import PluginManifest


class PluginProtocol(Protocol):
    @property
    def manifest(self) -> PluginManifest: ...
