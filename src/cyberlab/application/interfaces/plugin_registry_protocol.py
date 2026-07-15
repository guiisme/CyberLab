from __future__ import annotations

from typing import Protocol

from cyberlab.application.interfaces.plugin_protocol import PluginProtocol


class PluginRegistryProtocol(Protocol):
    def register(
        self,
        plugin: PluginProtocol,
    ) -> None: ...

    def get(
        self,
        plugin_id: str,
    ) -> PluginProtocol | None: ...

    def has(
        self,
        plugin_id: str,
    ) -> bool: ...

    def list(
        self,
    ) -> list[PluginProtocol]: ...
