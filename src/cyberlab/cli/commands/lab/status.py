from __future__ import annotations

import typer

from cyberlab.application.interfaces.lab_lifecycle_protocol import LabLifeCycleProtocol
from cyberlab.application.use_cases.get_lab_status_use_case import (
    GetLabStatusUseCase,
)


def register_status_command(
    app: typer.Typer,
    lab_status: LabLifeCycleProtocol,
) -> None:
    """Register the 'lab status' command."""

    @app.command("status")
    def status(
        lab_id: str,
    ) -> None:
        """Show the status of a laboratory."""

        laboratory_status = GetLabStatusUseCase(
            lab_status,
        ).execute(
            lab_id,
        )

        typer.echo(f"Laboratory: {lab_id}")
        typer.echo(f"Status: {laboratory_status}")
