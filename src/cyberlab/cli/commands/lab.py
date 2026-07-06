from __future__ import annotations

from pathlib import Path

import typer

from cyberlab.application.use_cases.list_labs_use_case import (
    ListLabsUseCase,
)
from cyberlab.infrastructure.filesystem.filesystem_lab_repository import (
    FilesystemLabRepository,
)


def register_lab(app: typer.Typer) -> None:
    """Register lab commands."""

    @app.command("lab-list")
    def lab_list() -> None:
        """List available CyberLab laboratories."""

        repository = FilesystemLabRepository(
            labs_root=Path("labs"),
        )

        use_case = ListLabsUseCase(
            repository=repository,
        )

        labs = use_case.execute()

        if not labs:
            typer.echo("No laboratories found.")
            return

        typer.echo("Available laboratories:")
        typer.echo()

        for lab in labs:
            typer.echo(f"- {lab.name}")
