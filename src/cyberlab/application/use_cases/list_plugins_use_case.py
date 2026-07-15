from __future__ import annotations

from cyberlab.application.interfaces.plugin_protocol import (
    PluginProtocol,
)
from cyberlab.application.interfaces.plugin_registry_protocol import PluginRegistryProtocol


class ListPluginsUseCase:
    def __init__(
        self,
        registry: PluginRegistryProtocol,
    ) -> None:
        self._registry = registry

    def execute(
        self,
    ) -> list[PluginProtocol]:
        return self._registry.list()
