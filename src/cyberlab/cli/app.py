from __future__ import annotations

from pathlib import Path

import typer

from cyberlab.application.interfaces.command_runner_protocol import (
    CommandRunnerProtocol,
)
from cyberlab.application.interfaces.lab_manifest_loader_protocol import (
    LabManifestLoaderProtocol,
)
from cyberlab.application.interfaces.lab_validator_protocol import LabValidatorProtocol
from cyberlab.cli.commands.doctor import register_doctor
from cyberlab.cli.commands.lab import register_lab
from cyberlab.cli.commands.version import register_version
from cyberlab.infrastructure.filesystem.filesystem_lab_validator import FilesystemLabValidator
from cyberlab.infrastructure.filesystem.yaml_lab_manifest_loader import (
    YamlLabManifestLoader,
)
from cyberlab.infrastructure.process.command_runner import CommandRunner


def create_app(
    runner: CommandRunnerProtocol | None = None,
    manifest_loader: LabManifestLoaderProtocol | None = None,
    validator: LabValidatorProtocol | None = None,
) -> typer.Typer:
    """Create the CyberLab CLI application."""

    app = typer.Typer(
        help="CyberLab - Reproducible Cybersecurity Labs",
    )

    runner = runner or CommandRunner()

    manifest_loader = manifest_loader or YamlLabManifestLoader(
        labs_root=Path("labs"),
    )

    validator = validator or FilesystemLabValidator(
        labs_root=Path("labs"),
    )

    register_version(app)
    register_doctor(app, runner)
    register_lab(
        app,
        manifest_loader,
        validator,
    )

    return app


app = create_app()


def main() -> None:
    app()
