from __future__ import annotations

import typer

from cyberlab.application.use_cases.version import (
    get_version as get_application_version,
)


def register(app: typer.Typer) -> None:
    """Register the version command."""

    @app.command("version")
    def version() -> None:
        """Show the current CyberLab version."""

        typer.echo(get_application_version())
