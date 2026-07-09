from __future__ import annotations

import typer

from cyberlab.application.interfaces.lab_repository_protocol import (
    LabRepositoryProtocol,
)
from cyberlab.application.use_cases.list_labs_use_case import (
    ListLabsUseCase,
)


def register_list_command(
    app: typer.Typer,
    repository: LabRepositoryProtocol,
) -> None:
    """Register the 'lab list' command."""

    @app.command("list")
    def list_labs() -> None:
        """List available laboratories."""

        laboratories = ListLabsUseCase(
            repository,
        ).execute()

        if not laboratories:
            typer.echo("No laboratories found.")
            return

        typer.echo("Available laboratories:")
        typer.echo()

        for laboratory in laboratories:
            typer.echo(f"- {laboratory.name}")
