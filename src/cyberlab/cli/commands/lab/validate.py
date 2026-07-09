from __future__ import annotations

import typer

from cyberlab.application.interfaces.lab_validator_protocol import (
    LabValidatorProtocol,
)
from cyberlab.application.use_cases.lab_validation_use_case import (
    LabValidationUseCase,
)
from cyberlab.cli.rendering.checks import (
    render_checks,
)


def register_validate_command(
    app: typer.Typer,
    validator: LabValidatorProtocol,
) -> None:
    """Register the 'lab validate' command."""

    @app.command("validate")
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
