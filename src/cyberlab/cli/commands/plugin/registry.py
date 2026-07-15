from __future__ import annotations

import typer

from cyberlab.application.use_cases.create_plugin_use_case import (
    CreatePluginUseCase,
)
from cyberlab.application.use_cases.list_plugins_use_case import (
    ListPluginsUseCase,
)
from cyberlab.cli.commands.plugin.create import (
    create_command,
)
from cyberlab.cli.commands.plugin.init import (
    init_plugin_command,
)
from cyberlab.cli.commands.plugin.plugin_list import (
    list_command,
)


def register_plugin_commands(
    app: typer.Typer,
    list_plugins: ListPluginsUseCase,
    create_plugin: CreatePluginUseCase,
) -> None:
    """Register plugin commands."""

    plugin_app = typer.Typer(
        help="Plugin management commands.",
    )

    plugin_app.command(
        "list",
    )(
        list_command(
            list_plugins,
        )
    )

    plugin_app.command(
        "create",
    )(
        create_command(
            create_plugin,
        )
    )
    plugin_app.command(
        "init",
    )(init_plugin_command())

    app.add_typer(
        plugin_app,
        name="plugin",
    )
