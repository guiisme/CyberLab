from __future__ import annotations

import typer

from cyberlab.application.interfaces.command_runner_protocol import (
    CommandRunnerProtocol,
)
from cyberlab.application.use_cases.doctor_use_case import DoctorUseCase
from cyberlab.cli.rendering.checks import render_checks


def register_doctor(
    app: typer.Typer,
    runner: CommandRunnerProtocol,
) -> None:
    """Register doctor commands."""

    @app.command()
    def doctor() -> None:
        """Validate the local environment."""

        report = DoctorUseCase(
            runner,
        ).execute()

        render_checks(report.checks)

        typer.echo()

        if report.success:
            typer.echo("Environment OK")
        else:
            typer.echo("Environment has issues")
