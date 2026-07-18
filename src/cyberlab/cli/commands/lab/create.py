from __future__ import annotations

import typer

from cyberlab.application.interfaces.lab_scaffolding_protocol import (
    LabScaffoldingProtocol,
)
from cyberlab.application.use_cases.lab_create_use_case import (
    LabCreateUseCase,
)

KALI_PROFILES = ("minimal", "web", "network")


def register_create_command(
    app: typer.Typer,
    lab_scaffolding: LabScaffoldingProtocol,
) -> None:
    """Register the 'lab create' command."""

    @app.command("create")
    def create(
        lab_id: str,
        template: str = typer.Option("default", "--template", "-t"),
        profile: str = typer.Option("web", "--profile"),
    ) -> None:
        """Create a new laboratory."""

        if template == "kali" and profile not in KALI_PROFILES:
            available_profiles = ", ".join(KALI_PROFILES)
            raise typer.BadParameter(
                f"Perfil Kali inválido: '{profile}'. Disponíveis: {available_profiles}.",
                param_hint="--profile",
            )

        typer.echo(f'Creating laboratory "{lab_id}"...')

        typer.echo()

        LabCreateUseCase(
            lab_scaffolding,
        ).execute(
            lab_id,
            scaffold=template,
            profile=profile,
        )

        typer.echo(
            f'✔ Laboratory "{lab_id}" created successfully.',
        )
