from __future__ import annotations

import typer

from cyberlab.application.interfaces.command_runner_protocol import (
    CommandRunnerProtocol,
)
from cyberlab.application.interfaces.lab_lifecycle_protocol import (
    LabLifeCycleProtocol,
)
from cyberlab.application.interfaces.lab_manifest_loader_protocol import (
    LabManifestLoaderProtocol,
)
from cyberlab.application.interfaces.lab_repository_protocol import (
    LabRepositoryProtocol,
)
from cyberlab.application.interfaces.lab_scaffolding_protocol import (
    LabScaffoldingProtocol,
)
from cyberlab.application.interfaces.lab_validator_protocol import (
    LabValidatorProtocol,
)
from cyberlab.application.use_cases.create_plugin_use_case import (
    CreatePluginUseCase,
)
from cyberlab.application.use_cases.list_plugins_use_case import (
    ListPluginsUseCase,
)
from cyberlab.cli.commands.doctor import (
    register_doctor,
)
from cyberlab.cli.commands.lab.registry import (
    register_lab_commands,
)
from cyberlab.cli.commands.plugin.registry import (
    register_plugin_commands,
)
from cyberlab.cli.commands.version import (
    register_version,
)
from podman.src.cyberlab_plugin_podman.infrastructure.podman_compose import (
    PodmanComposeLabLifecycle,
)

lifecycle_adapter = PodmanComposeLabLifecycle()


def register_commands(
    app: typer.Typer,
    runner: CommandRunnerProtocol,
    repository: LabRepositoryProtocol,
    manifest_loader: LabManifestLoaderProtocol,
    validator: LabValidatorProtocol,
    lab_runner: LabLifeCycleProtocol,
    lab_scaffolding: LabScaffoldingProtocol,
    list_plugins: ListPluginsUseCase,
    create_plugin: CreatePluginUseCase,
) -> None:
    """Register all CLI commands."""

    register_version(app)

    register_doctor(
        app,
        runner,
    )

    register_lab_commands(
        app=app,
        repository=repository,
        validator=validator,
        manifest_loader=manifest_loader,
        # lifecycle=lifecycle,
        lab_scaffolding=lab_scaffolding,
        lab_runner=lab_runner,
    )

    register_plugin_commands(
        app=app,
        list_plugins=list_plugins,
        create_plugin=create_plugin,
    )
