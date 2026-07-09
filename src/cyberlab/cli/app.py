from __future__ import annotations

from pathlib import Path

import typer

from cyberlab.application.interfaces.command_runner_protocol import (
    CommandRunnerProtocol,
)
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
from cyberlab.cli.commands.registry import (
    register_commands,
)
from cyberlab.infrastructure.docker.docker_compose_lab_runner import (
    DockerComposeLabRunner,
)
from cyberlab.infrastructure.docker.docker_compose_service import (
    DockerComposeService,
)
from cyberlab.infrastructure.filesystem.filesystem_lab_repository import (
    FilesystemLabRepository,
)
from cyberlab.infrastructure.filesystem.filesystem_lab_validator import (
    FilesystemLabValidator,
)
from cyberlab.infrastructure.filesystem.yaml_lab_manifest_loader import (
    YamlLabManifestLoader,
)
from cyberlab.infrastructure.process.command_runner import (
    CommandRunner,
)


def create_app(
    command_runner: CommandRunnerProtocol | None = None,
    repository: LabRepositoryProtocol | None = None,
    manifest_loader: LabManifestLoaderProtocol | None = None,
    validator: LabValidatorProtocol | None = None,
    lab_runner: LabRunnerProtocol | None = None,
) -> typer.Typer:
    """Create the CyberLab CLI application."""

    app = typer.Typer(
        help="CyberLab command-line interface.",
    )

    labs_root = Path("labs")

    command_runner = command_runner or CommandRunner()

    repository = repository or FilesystemLabRepository(
        labs_root=labs_root,
    )

    manifest_loader = manifest_loader or YamlLabManifestLoader(
        labs_root=labs_root,
    )

    validator = validator or FilesystemLabValidator(
        labs_root=labs_root,
    )

    docker_compose_service = DockerComposeService(
        command_runner,
    )

    lab_runner = lab_runner or DockerComposeLabRunner(
        compose_service=docker_compose_service,
        labs_root=labs_root,
    )

    register_commands(
        app=app,
        runner=command_runner,
        repository=repository,
        manifest_loader=manifest_loader,
        validator=validator,
        lab_runner=lab_runner,
    )

    return app


app = create_app()
