from __future__ import annotations

import typer

from cyberlab.application.interfaces.lab_scaffolding_protocol import (
    LabScaffoldingProtocol,
)
from cyberlab.application.use_cases.lab_create_use_case import (
    LabCreateUseCase,
)


def register_create_command(
    app: typer.Typer,
    lab_scaffolding: LabScaffoldingProtocol,
) -> None:
    """Register the 'lab create' command."""

    @app.command("create")
    def create(
        lab_id: str,
    ) -> None:
        """Create a new laboratory."""

        typer.echo(f'Creating laboratory "{lab_id}"...')

        typer.echo()

        LabCreateUseCase(
            lab_scaffolding,
        ).execute(
            lab_id,
        )

        typer.echo(
            f'✔ Laboratory "{lab_id}" created successfully.',
        )
