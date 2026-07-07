from __future__ import annotations

import typer

from cyberlab.application.interfaces.lab_manifest_loader_protocol import (
    LabManifestLoaderProtocol,
)
from cyberlab.application.interfaces.lab_repository_protocol import (
    LabRepositoryProtocol,
)
from cyberlab.application.interfaces.lab_runner_protocol import (
    LabRunnerProtocol,
)
from cyberlab.application.interfaces.lab_validator_protocol import (
    LabValidatorProtocol,
)
from cyberlab.application.use_cases.lab_info_use_case import (
    LabInfoUseCase,
)
from cyberlab.application.use_cases.lab_run_use_case import (
    LabRunUseCase,
)
from cyberlab.application.use_cases.lab_validation_use_case import (
    LabValidationUseCase,
)
from cyberlab.application.use_cases.list_labs_use_case import (
    ListLabsUseCase,
)
from cyberlab.cli.rendering.checks import (
    render_checks,
)


def register_lab(
    app: typer.Typer,
    repository: LabRepositoryProtocol,
    manifest_loader: LabManifestLoaderProtocol,
    validator: LabValidatorProtocol,
    lab_runner: LabRunnerProtocol,
) -> None:
    """Register laboratory commands."""

    lab_app = typer.Typer(
        help="Manage CyberLab laboratories.",
    )

    app.add_typer(
        lab_app,
        name="lab",
    )

    @lab_app.command("list")
    def list_labs() -> None:
        """List available laboratories."""

        use_case = ListLabsUseCase(
            repository,
        )

        laboratories = use_case.execute()

        if not laboratories:
            typer.echo("No laboratories found.")
            return

        typer.echo("Available laboratories:")
        typer.echo()

        for laboratory in laboratories:
            typer.echo(f"- {laboratory.name}")

    @lab_app.command("info")
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

    @lab_app.command("validate")
    def validate(
        lab_id: str,
    ) -> None:
        """Validate a laboratory."""

        report = LabValidationUseCase(
            validator,
        ).execute(
            lab_id,
        )

        render_checks(report.checks)

        typer.echo()

        if report.success:
            typer.echo("Laboratory is valid.")
        else:
            typer.echo("Laboratory validation failed.")

    @lab_app.command("run")
    def run(
        lab_id: str,
    ) -> None:
        """Run a laboratory."""

        typer.echo(f'Running laboratory "{lab_id}"...')

        typer.echo()

        report = LabRunUseCase(
            lab_runner,
        ).execute(
            lab_id,
        )

        icon = "✔" if report.success else "✘"

        typer.echo(f"{icon} {report.message}")
