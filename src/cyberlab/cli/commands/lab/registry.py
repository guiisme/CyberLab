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
from cyberlab.application.interfaces.lab_scaffolding_protocol import LabScaffoldingProtocol
from cyberlab.application.interfaces.lab_validator_protocol import (
    LabValidatorProtocol,
)
from cyberlab.cli.commands.lab.init import register_init_command
from podman.src.cyberlab_plugin_podman.infrastructure.podman_compose import (
    PodmanComposeLabLifecycle,
)

from .create import (
    register_create_command,
)
from .info import (
    register_info_command,
)
from .list import (
    register_list_command,
)
from .logs import (
    register_logs_command,
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


def register_lab_commands(
    app: typer.Typer,
    repository: LabRepositoryProtocol,
    manifest_loader: LabManifestLoaderProtocol,
    validator: LabValidatorProtocol,
    # O lab_runner aqui é o padrão do Core, mas vamos sobrescrevê-lo pelo seu adaptador
    lab_runner: LabLifeCycleProtocol,
    lab_scaffolding: LabScaffoldingProtocol,
) -> None:
    lab_app = typer.Typer(help="Manage CyberLab laboratories.")

    # Instanciamos o adaptador uma única vez aqui dentro
    # Isso garante que todos os comandos usem o MESMO comportamento de caminho
    runner = PodmanComposeLabLifecycle()

    # Registramos TODOS os comandos usando o mesmo 'runner' (o adaptador corrigido)
    register_run_command(lab_app, runner)
    register_stop_command(lab_app, runner)
    register_status_command(lab_app, runner)
    register_logs_command(lab_app, runner)
    register_restart_command(lab_app, runner)

    # Comandos que não dependem do runner continuam com seus protocolos originais
    register_list_command(lab_app, repository)
    register_info_command(lab_app, manifest_loader)
    register_validate_command(lab_app, validator)
    register_create_command(lab_app, lab_scaffolding)
    register_init_command(app=lab_app)

    app.add_typer(lab_app, name="lab")
