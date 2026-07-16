from __future__ import annotations

from pathlib import Path

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
from cyberlab.application.interfaces.lab_scaffolding_protocol import LabScaffoldingProtocol
from cyberlab.application.interfaces.lab_validator_protocol import (
    LabValidatorProtocol,
)
from cyberlab.application.interfaces.plugin_scaffolding_protocol import PluginScaffoldingProtocol
from cyberlab.application.use_cases.create_plugin_use_case import (
    CreatePluginUseCase,
)
from cyberlab.application.use_cases.list_plugins_use_case import (
    ListPluginsUseCase,
)
from cyberlab.cli.commands.registry import (
    register_commands,
)
from cyberlab.infrastructure.docker.docker_compose_lab_lifecycle import (
    DockerComposeLabRunner,
)
from cyberlab.infrastructure.docker.docker_compose_service import (
    DockerComposeService,
)
from cyberlab.infrastructure.filesystem.filesystem_lab_repository import (
    FilesystemLabRepository,
)
from cyberlab.infrastructure.filesystem.filesystem_lab_scaffolding import (
    FilesystemLabScaffolding,
)
from cyberlab.infrastructure.filesystem.filesystem_lab_validator import (
    FilesystemLabValidator,
)
from cyberlab.infrastructure.filesystem.filesystem_plugin_scaffolding import (
    FilesystemPluginScaffolding,
)
from cyberlab.infrastructure.filesystem.yaml_lab_manifest_loader import (
    YamlLabManifestLoader,
)

# Plugin infrastructure
from cyberlab.infrastructure.plugins.entry_point_provider import (
    EntryPointProvider,
)
from cyberlab.infrastructure.plugins.plugin_loader import (
    PluginLoader,
)
from cyberlab.infrastructure.plugins.plugin_registry import (
    PluginRegistry,
)
from cyberlab.infrastructure.process.command_runner import (
    CommandRunner,
)


def _create_plugin_registry() -> PluginRegistry:
    """Create and initialize the plugin registry."""

    registry = PluginRegistry()

    provider = EntryPointProvider()
    loader = PluginLoader(provider)

    for plugin in loader.load():
        registry.register(plugin)

    return registry


def create_app(
    command_runner: CommandRunnerProtocol | None = None,
    repository: LabRepositoryProtocol | None = None,
    manifest_loader: LabManifestLoaderProtocol | None = None,
    validator: LabValidatorProtocol | None = None,
    lab_runner: LabLifeCycleProtocol | None = None,
    lab_scaffolding: LabScaffoldingProtocol | None = None,
    plugin_scaffolding: PluginScaffoldingProtocol | None = None,
    plugin_registry: PluginRegistry | None = None,
) -> typer.Typer:
    """Create the CyberLab CLI application."""

    app = typer.Typer(
        help="CyberLab command-line interface.",
    )

    labs_root = Path(".")
    scaffolds_root = Path("scaffolds")
    plugin_templates_root = Path("templates/plugin")
    plugins_root = Path(".")

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

    lab_scaffolding = lab_scaffolding or FilesystemLabScaffolding(
        labs_root=labs_root,
        scaffolds_root=scaffolds_root,
    )

    plugin_scaffolding = plugin_scaffolding or FilesystemPluginScaffolding(
        plugins_root=plugins_root,
        plugin_scaffolds_root=plugin_templates_root,
    )

    plugin_registry = plugin_registry or _create_plugin_registry()

    list_plugins = ListPluginsUseCase(
        plugin_registry,
    )

    create_plugin = CreatePluginUseCase(
        plugin_scaffolding,
    )

    register_commands(
        app=app,
        runner=command_runner,
        repository=repository,
        manifest_loader=manifest_loader,
        validator=validator,
        lab_runner=lab_runner,
        lab_scaffolding=lab_scaffolding,
        list_plugins=list_plugins,
        create_plugin=create_plugin,
    )

    return app


app = create_app()
