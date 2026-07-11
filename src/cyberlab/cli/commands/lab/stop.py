from __future__ import annotations

import typer

from cyberlab.application.interfaces.lab_runner_protocol import (
    LabRunnerProtocol,
)
from cyberlab.application.use_cases.stop_lab_use_case import (
    LabStopUseCase,
)


def register_stop_command(
    app: typer.Typer,
    lab_runner: LabRunnerProtocol,
) -> None:
    """Register the 'lab stop' command."""

    @app.command("stop")
    def stop(
        lab_id: str,
    ) -> None:
        """Stop a laboratory."""

        typer.echo(f'Stopping laboratory "{lab_id}"...')

        typer.echo()

        report = LabStopUseCase(
            lab_runner,
        ).execute(
            lab_id,
        )

        icon = "✔" if report.success else "✘"

        typer.echo(f"{icon} {report.message}")
