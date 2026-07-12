from __future__ import annotations

import typer

from cyberlab.application.interfaces.lab_lifecycle_protocol import (
    LabLifeCycleProtocol,
)
from cyberlab.application.interfaces.lab_manifest_loader_protocol import (
    LabManifestLoaderProtocol,
)
from cyberlab.application.interfaces.lab_repository_protocol import (
    LabRepositoryProtocol,
)
from cyberlab.application.interfaces.lab_validator_protocol import (
    LabValidatorProtocol,
)

from .info import (
    register_info_command,
)
from .list import (
    register_list_command,
)
from .restart import (
    register_restart_command,
)
from .run import (
    register_run_command,
)
from .status import (
    register_status_command,
)
from .stop import (
    register_stop_command,
)
from .validate import (
    register_validate_command,
)


def register_lab(
    app: typer.Typer,
    repository: LabRepositoryProtocol,
    manifest_loader: LabManifestLoaderProtocol,
    validator: LabValidatorProtocol,
    lab_runner: LabLifeCycleProtocol,
) -> None:
    """Register laboratory commands."""

    lab_app = typer.Typer(
        help="Manage CyberLab laboratories.",
    )

    register_list_command(
        lab_app,
        repository,
    )

    register_info_command(
        lab_app,
        manifest_loader,
    )

    register_validate_command(
        lab_app,
        validator,
    )

    register_run_command(
        lab_app,
        lab_runner,
    )

    register_stop_command(
        lab_app,
        lab_runner,
    )

    register_status_command(
        lab_app,
        lab_runner,
    )

    register_restart_command(
        lab_app,
        lab_runner,
    )

    app.add_typer(
        lab_app,
        name="lab",
    )
