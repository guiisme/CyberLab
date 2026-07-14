from rich.console import Console
from rich.table import Table

from cyberlab.application.interfaces.plugin_registry_protocol import (
    PluginRegistryProtocol,
)

console = Console()


def plugin_list(
    registry: PluginRegistryProtocol,
) -> None:
    """List installed plugins."""

    table = Table(title="Installed Plugins")

    table.add_column("ID")
    table.add_column("Version")
    table.add_column("Author")

    for plugin in registry.all():
        manifest = plugin.manifest

        table.add_row(
            manifest.id,
            manifest.version,
            manifest.author,
        )

    console.print(table)
