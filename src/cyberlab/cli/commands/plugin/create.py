from __future__ import annotations

from collections.abc import Callable

import typer

from cyberlab.application.use_cases.create_plugin_use_case import (
    CreatePluginUseCase,
)


def create_command(
    use_case: CreatePluginUseCase,
) -> Callable[..., None]:
    """Create the plugin creation command."""

    def command(
        plugin_id: str = typer.Argument(
            ...,
            help="Plugin identifier.",
        ),
    ) -> None:
        """Create a new plugin project."""

        use_case.execute(
            plugin_id=plugin_id,
        )

        typer.secho(
            f'Plugin "{plugin_id}" created successfully.',
            fg=typer.colors.GREEN,
        )
        typer.echo(
            f"Install it in the CyberLab environment with:\n"
            f"  uv pip install --no-deps -e ./{plugin_id}",
        )

    return command
