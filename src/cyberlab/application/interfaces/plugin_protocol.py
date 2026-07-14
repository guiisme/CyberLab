from __future__ import annotations

from typing import Protocol, runtime_checkable

from cyberlab.domain.models.plugin_manifest import PluginManifest


@runtime_checkable
class PluginProtocol(Protocol):
    @property
    def manifest(self) -> PluginManifest: ...
