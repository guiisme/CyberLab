from collections.abc import Sequence

from cyberlab.application.interfaces.plugin_protocol import PluginProtocol
from cyberlab.application.interfaces.plugin_registry_protocol import (
    PluginRegistryProtocol,
)


class PluginRegistry(PluginRegistryProtocol):
    """In-memory registry for loaded plugins."""

    def __init__(self) -> None:
        self._plugins: dict[str, PluginProtocol] = {}

    def register(self, plugin: PluginProtocol) -> None:
        plugin_id = plugin.manifest.id

        if plugin_id in self._plugins:
            raise ValueError(f"Plugin '{plugin_id}' is already registered.")

        self._plugins[plugin_id] = plugin

    def all(self) -> Sequence[PluginProtocol]:
        return tuple(self._plugins.values())

    def get(self, plugin_id: str) -> PluginProtocol | None:
        return self._plugins.get(plugin_id)

    def has(self, plugin_id: str) -> bool:
        return plugin_id in self._plugins

    def plugins(self) -> Sequence[PluginProtocol]:
        raise NotImplementedError
