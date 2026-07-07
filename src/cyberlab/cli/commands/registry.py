from __future__ import annotations

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
from cyberlab.cli.commands.doctor import (
    register_doctor,
)
from cyberlab.cli.commands.lab import (
    register_lab,
)
from cyberlab.cli.commands.version import (
    register_version,
)


def register_commands(
    app: typer.Typer,
    runner: CommandRunnerProtocol,
    repository: LabRepositoryProtocol,
    manifest_loader: LabManifestLoaderProtocol,
    validator: LabValidatorProtocol,
    lab_runner: LabRunnerProtocol,
) -> None:
    """Register all CLI commands."""

    register_version(app)

    register_doctor(
        app,
        runner,
    )

    register_lab(
        app,
        repository,
        manifest_loader,
        validator,
        lab_runner,
    )
