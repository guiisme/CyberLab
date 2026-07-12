from __future__ import annotations

import typer

from cyberlab.application.interfaces.lab_lifecycle_protocol import (
    LabLifeCycleProtocol,
)
from cyberlab.application.use_cases.lab_logs_use_case import (
    LabLogsUseCase,
)


def register_logs_command(
    app: typer.Typer,
    lab_runner: LabLifeCycleProtocol,
) -> None:
    """Register the 'lab logs' command."""

    @app.command("logs")
    def logs(
        lab_id: str,
    ) -> None:
        """Show laboratory logs."""

        typer.echo(f'Showing logs for laboratory "{lab_id}"...')

        typer.echo()

        logs = LabLogsUseCase(
            lab_runner,
        ).execute(
            lab_id,
        )

        typer.echo(logs.content)
