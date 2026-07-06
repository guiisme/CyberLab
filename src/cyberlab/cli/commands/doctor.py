from __future__ import annotations

import typer

from cyberlab.application.interfaces.command_runner_protocol import (
    CommandRunnerProtocol,
)
from cyberlab.application.use_cases.doctor import DoctorUseCase


def register(
    app: typer.Typer,
    runner: CommandRunnerProtocol,
) -> None:
    """Register the doctor command."""

    @app.command("doctor")
    def doctor() -> None:
        """Validate the local environment."""

        use_case = DoctorUseCase(runner)

        report = use_case.execute()

        for check in report.checks:
            status = "OK" if check.success else "FAIL"
            typer.echo(f"[{status}] {check.name}: {check.message}")

        raise typer.Exit(code=0 if report.success else 1)
