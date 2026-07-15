from __future__ import annotations

from typing import Protocol


class PluginScaffoldingProtocol(Protocol):
    def create(
        self,
        plugin_id: str,
        plugin_scaffold: str = "default",
    ) -> None: ...
