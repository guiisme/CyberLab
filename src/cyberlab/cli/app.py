from __future__ import annotations

import typer

from cyberlab.application.interfaces.command_runner_protocol import (
    CommandRunnerProtocol,
)
from cyberlab.cli.commands.registry import register_commands
from cyberlab.infrastructure.process.command_runner import CommandRunner


def create_app(
    runner: CommandRunnerProtocol | None = None,
) -> typer.Typer:
    """Create the CyberLab CLI application."""

    if runner is None:
        runner = CommandRunner()

    app = typer.Typer(
        help="CyberLab command-line interface.",
        no_args_is_help=True,
    )

    register_commands(app, runner)

    return app
