from __future__ import annotations

import typer

from cyberlab.application.use_cases.version_use_case import (
    VersionUseCase,
)


def register_version(
    app: typer.Typer,
) -> None:
    """Register version commands."""

    @app.command()
    def version() -> None:
        typer.echo(
            VersionUseCase().execute(),
        )
