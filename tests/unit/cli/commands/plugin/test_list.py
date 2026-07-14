from cyberlab.application.interfaces.plugin_protocol import PluginProtocol
from cyberlab.application.interfaces.plugin_registry_protocol import PluginRegistryProtocol


class FakePluginRegistry(PluginRegistryProtocol):
    def __init__(self) -> None:
        self._plugins: list[PluginProtocol] = []

    def register(self, plugin: PluginProtocol) -> None:
        self._plugins.append(plugin)

    def all(self) -> tuple[PluginProtocol, ...]:
        return tuple(self._plugins)

    def get(self, plugin_id: str): ...

    def has(self, plugin_id: str) -> bool: ...
