from __future__ import annotations

import typer

from cyberlab.application.interfaces.command_runner_protocol import (
    CommandRunnerProtocol,
)
from cyberlab.cli.commands.doctor import register_doctor
from cyberlab.cli.commands.lab import register_lab
from cyberlab.cli.commands.version import register_version
from cyberlab.infrastructure.process.command_runner import (
    CommandRunner,
)


def create_app(
    runner: CommandRunnerProtocol | None = None,
) -> typer.Typer:
    """Create the CyberLab CLI application."""

    app = typer.Typer(
        help="CyberLab - Reproducible Cybersecurity Labs",
    )

    runner = runner or CommandRunner()

    register_version(app)
    register_doctor(app, runner)
    register_lab(app)

    return app


app = create_app()


def main() -> None:
    app()


if __name__ == "__main__":
    main()
