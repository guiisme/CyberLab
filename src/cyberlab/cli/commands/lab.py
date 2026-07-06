from __future__ import annotations

from pathlib import Path

import typer

from cyberlab.application.interfaces.lab_manifest_loader_protocol import (
    LabManifestLoaderProtocol,
)
from cyberlab.application.use_cases.lab_info_use_case import (
    LabInfoUseCase,
)
from cyberlab.application.use_cases.list_labs_use_case import (
    ListLabsUseCase,
)
from cyberlab.infrastructure.filesystem.filesystem_lab_repository import (
    FilesystemLabRepository,
)


def register_lab(
    app: typer.Typer,
    manifest_loader: LabManifestLoaderProtocol,
) -> None:
    """Register lab commands."""

    lab_app = typer.Typer(
        help="Manage CyberLab laboratories.",
    )

    @lab_app.command("list")
    def list_labs() -> None:
        """List available laboratories."""

        repository = FilesystemLabRepository(
            labs_root=Path("labs"),
        )

        use_case = ListLabsUseCase(repository)

        labs = use_case.execute()

        if not labs:
            typer.echo("No laboratories found.")
            return

        typer.echo("Available laboratories:")
        typer.echo()

        for lab in labs:
            typer.echo(f"- {lab.name}")

    @lab_app.command("info")
    def info(
        lab_id: str,
    ) -> None:
        """Show laboratory metadata."""

        manifest = LabInfoUseCase(
            manifest_loader,
        ).execute(
            lab_id,
        )

        typer.echo(f"Name: {manifest.name}")
        typer.echo(f"ID: {manifest.id}")
        typer.echo(f"Category: {manifest.category}")
        typer.echo(f"Difficulty: {manifest.difficulty}")
        typer.echo(f"Version: {manifest.version}")
        typer.echo()
        typer.echo("Description:")
        typer.echo(manifest.description)

    app.add_typer(
        lab_app,
        name="lab",
    )
