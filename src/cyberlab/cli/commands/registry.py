from __future__ import annotations

import typer

from cyberlab.application.interfaces.command_runner_protocol import (
    CommandRunnerProtocol,
)
from cyberlab.cli.commands.doctor import register as register_doctor
from cyberlab.cli.commands.version import register as register_version


def register_commands(
    app: typer.Typer,
    runner: CommandRunnerProtocol,
) -> None:
    """Register all CLI commands."""

    register_version(app)
    register_doctor(app, runner)
