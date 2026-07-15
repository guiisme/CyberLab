from __future__ import annotations

from cyberlab.application.interfaces.plugin_scaffolding_protocol import (
    PluginScaffoldingProtocol,
)


class CreatePluginUseCase:
    """Create a new plugin project from the official template."""

    def __init__(
        self,
        scaffolding: PluginScaffoldingProtocol,
    ) -> None:
        self._scaffolding = scaffolding

    def execute(
        self,
        plugin_id: str,
    ) -> None:
        """Create a new plugin project."""

        self._scaffolding.create(
            plugin_id=plugin_id,
        )
