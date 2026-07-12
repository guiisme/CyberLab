from __future__ import annotations

import typer

from cyberlab.application.interfaces.lab_lifecycle_protocol import (
    LabLifeCycleProtocol,
)
from cyberlab.application.use_cases.lab_restart_use_case import LabRestartUseCase


def register_restart_command(
    app: typer.Typer,
    lab_runner: LabLifeCycleProtocol,
) -> None:
    """Register the 'lab restart' command."""

    @app.command("restart")
    def restart(
        lab_id: str,
    ) -> None:
        """Restart a laboratory."""

        typer.echo(f'Restarting laboratory "{lab_id}"...')

        typer.echo()

        report = LabRestartUseCase(
            lab_runner,
        ).execute(
            lab_id,
        )

        icon = "✔" if report.success else "✘"

        typer.echo(f"{icon} {report.message}")
