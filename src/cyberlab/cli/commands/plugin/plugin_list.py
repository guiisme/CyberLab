from __future__ import annotations

from collections.abc import Callable

from rich.console import Console
from rich.table import Table

from cyberlab.application.use_cases.list_plugins_use_case import (
    ListPluginsUseCase,
)


def list_command(
    use_case: ListPluginsUseCase,
) -> Callable[..., None]:
    """Create the plugin list command."""

    def command() -> None:
        """List installed plugins."""

        plugins = use_case.execute()

        table = Table(title="Installed Plugins")

        table.add_column("ID")
        table.add_column("Version")
        table.add_column("Author")

        for plugin in plugins:
            manifest = plugin.manifest

            table.add_row(
                manifest.id,
                manifest.version,
                manifest.author,
            )

        Console().print(table)

    return command
