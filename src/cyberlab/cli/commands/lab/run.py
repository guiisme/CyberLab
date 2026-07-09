from __future__ import annotations

import typer

from cyberlab.application.interfaces.lab_runner_protocol import (
    LabRunnerProtocol,
)
from cyberlab.application.use_cases.lab_run_use_case import (
    LabRunUseCase,
)


def register_run_command(
    app: typer.Typer,
    lab_runner: LabRunnerProtocol,
) -> None:
    """Register the 'lab run' command."""

    @app.command("run")
    def run(
        lab_id: str,
    ) -> None:
        """Run a laboratory."""

        typer.echo(f'Running laboratory "{lab_id}"...')

        typer.echo()

        report = LabRunUseCase(
            lab_runner,
        ).execute(
            lab_id,
        )

        icon = "✔" if report.success else "✘"

        typer.echo(f"{icon} {report.message}")
