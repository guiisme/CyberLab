from importlib.metadata import EntryPoint
from typing import Any

from cyberlab.application.interfaces.plugin_loader_protocol import (
    PluginLoaderProtocol,
)
from cyberlab.application.interfaces.plugin_protocol import PluginProtocol
from cyberlab.infrastructure.plugins.entry_point_provider import (
    EntryPointProvider,
)


class PluginLoader(PluginLoaderProtocol):
    """Loads CyberLab plugins from Python entry points."""

    def __init__(
        self,
        provider: EntryPointProvider,
    ) -> None:
        self._provider = provider

    def load(self) -> tuple[PluginProtocol, ...]:
        plugins: list[PluginProtocol] = []

        for entry_point in self._provider.entry_points():
            plugin = self._load_plugin(entry_point)

            if plugin is not None:
                plugins.append(plugin)

        return tuple(plugins)

    def _load_plugin(
        self,
        entry_point: EntryPoint,
    ) -> PluginProtocol | None:
        try:
            plugin_class: Any = entry_point.load()
            plugin = plugin_class()

            if not isinstance(plugin, PluginProtocol):
                return None

            return plugin

        except Exception:
            return None
