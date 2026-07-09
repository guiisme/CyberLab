from __future__ import annotations

import typer

from cyberlab.application.interfaces.lab_manifest_loader_protocol import (
    LabManifestLoaderProtocol,
)
from cyberlab.application.use_cases.lab_info_use_case import (
    LabInfoUseCase,
)


def register_info_command(
    app: typer.Typer,
    manifest_loader: LabManifestLoaderProtocol,
) -> None:
    """Register the 'lab info' command."""

    @app.command("info")
    def info(
        lab_id: str,
    ) -> None:
        """Show laboratory information."""

        manifest = LabInfoUseCase(
            manifest_loader,
        ).execute(
            lab_id,
        )

        typer.echo(f"Name: {manifest.name}")
        typer.echo(f"Category: {manifest.category}")
        typer.echo(f"Difficulty: {manifest.difficulty}")
        typer.echo(f"Version: {manifest.version}")
