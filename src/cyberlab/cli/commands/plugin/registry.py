from __future__ import annotations

import typer

from cyberlab.application.interfaces.plugin_registry_protocol import (
    PluginRegistryProtocol,
)

from .list import plugin_list as list_plugins


def register_plugin_commands(
    app: typer.Typer,
    registry: PluginRegistryProtocol,
) -> None:
    """Register plugin CLI commands."""

    plugin_app = typer.Typer(
        help="Manage CyberLab plugins.",
    )

    @plugin_app.command("list")
    def list_command() -> None:
        """List installed plugins."""
        list_plugins(registry)

    app.add_typer(
        plugin_app,
        name="plugin",
    )
