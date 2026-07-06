from __future__ import annotations

import typer

from cyberlab.application.interfaces.command_runner_protocol import (
    CommandRunnerProtocol,
)
from cyberlab.application.use_cases.doctor_use_case import (
    DoctorUseCase,
)


def register_doctor(
    app: typer.Typer,
    runner: CommandRunnerProtocol,
) -> None:
    """Register doctor commands."""

    @app.command()
    def doctor() -> None:
        report = DoctorUseCase(runner).execute()

        for check in report.checks:
            icon = "✔" if check.success else "✘"
            typer.echo(f"{icon} {check.name}")

        typer.echo()

        typer.echo("Environment OK" if report.success else "Environment has issues")
