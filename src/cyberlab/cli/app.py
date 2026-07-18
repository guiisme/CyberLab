"""CyberLab command-line application composition root."""

from __future__ import annotations

from pathlib import Path

import typer

from cyberlab.application.interfaces.command_runner_protocol import CommandRunnerProtocol
from cyberlab.application.use_cases.create_plugin_use_case import CreatePluginUseCase
from cyberlab.application.use_cases.list_plugins_use_case import ListPluginsUseCase
from cyberlab.cli.commands.doctor import register_doctor
from cyberlab.cli.commands.lab.create import register_create_command
from cyberlab.cli.commands.lab.info import register_info_command
from cyberlab.cli.commands.lab.init import register_init_command
from cyberlab.cli.commands.lab.list import register_list_command
from cyberlab.cli.commands.lab.logs import register_logs_command
from cyberlab.cli.commands.lab.operations import register_operations_commands
from cyberlab.cli.commands.lab.restart import register_restart_command
from cyberlab.cli.commands.lab.run import register_run_command
from cyberlab.cli.commands.lab.status import register_status_command
from cyberlab.cli.commands.lab.stop import register_stop_command
from cyberlab.cli.commands.lab.validate import register_validate_command
from cyberlab.cli.commands.plugin.registry import register_plugin_commands
from cyberlab.cli.commands.version import register_version
from cyberlab.cli.legacy import main as legacy_main
from cyberlab.infrastructure.docker.docker_compose_lab_lifecycle import DockerComposeLabRunner
from cyberlab.infrastructure.docker.docker_compose_service import DockerComposeService
from cyberlab.infrastructure.environment import CYBERLAB_HOME
from cyberlab.infrastructure.filesystem.filesystem_lab_repository import FilesystemLabRepository
from cyberlab.infrastructure.filesystem.filesystem_lab_scaffolding import FilesystemLabScaffolding
from cyberlab.infrastructure.filesystem.filesystem_lab_validator import FilesystemLabValidator
from cyberlab.infrastructure.filesystem.filesystem_plugin_scaffolding import (
    FilesystemPluginScaffolding,
)
from cyberlab.infrastructure.filesystem.yaml_lab_manifest_loader import YamlLabManifestLoader
from cyberlab.infrastructure.lifecycle.engine_lab_lifecycle import EngineLabLifecycle
from cyberlab.infrastructure.plugins.entry_point_provider import EntryPointProvider
from cyberlab.infrastructure.plugins.plugin_loader import PluginLoader
from cyberlab.infrastructure.plugins.plugin_registry import PluginRegistry
from cyberlab.infrastructure.process.command_runner import CommandRunner
from cyberlab_plugin_k8s.infrastructure.k8s_lifecycle import KubernetesLifecycle
from cyberlab_plugin_podman.infrastructure.podman_compose import PodmanComposeLabLifecycle


def _repository_root() -> Path:
    return Path(__file__).resolve().parents[3]


def create_app(
    command_runner: CommandRunnerProtocol | None = None,
    *,
    labs_root: Path | None = None,
) -> typer.Typer:
    """Build the CLI and wire its adapters to application use cases.

    Optional dependencies make the composition root testable without invoking
    Docker, the filesystem outside a temporary directory, or installed plugins.
    """

    runner = command_runner or CommandRunner()
    root = _repository_root()
    resolved_labs_root = labs_root or CYBERLAB_HOME / "labs"

    app = typer.Typer(
        name="cyberlab",
        help="Framework for reproducible cybersecurity laboratories.",
        no_args_is_help=True,
    )
    lab_app = typer.Typer(help="Create, inspect, validate, and run laboratories.")

    register_doctor(app, runner)
    register_version(app)

    lab_repository = FilesystemLabRepository(resolved_labs_root)
    lab_scaffolding = FilesystemLabScaffolding(
        labs_root=resolved_labs_root,
        scaffolds_root=root / "scaffolds",
    )
    manifest_loader = YamlLabManifestLoader(resolved_labs_root)
    lab_validator = FilesystemLabValidator(resolved_labs_root)
    docker_lifecycle = DockerComposeLabRunner(
        compose_service=DockerComposeService(runner),
        labs_root=resolved_labs_root,
    )
    lifecycle = EngineLabLifecycle(
        resolved_labs_root,
        {
            "docker": lambda _lab_id: docker_lifecycle,
            "compose": lambda _lab_id: docker_lifecycle,
            "k8s": KubernetesLifecycle,
            "podman": lambda _lab_id: PodmanComposeLabLifecycle(),
        },
    )

    register_create_command(lab_app, lab_scaffolding)
    register_info_command(lab_app, manifest_loader)
    register_init_command(lab_app)
    register_list_command(lab_app, lab_repository)
    register_logs_command(lab_app, lifecycle)
    register_operations_commands(lab_app, lifecycle)
    register_restart_command(lab_app, lifecycle)
    register_run_command(lab_app, lifecycle)
    register_status_command(lab_app, lifecycle)
    register_stop_command(lab_app, lifecycle)
    register_validate_command(lab_app, lab_validator)
    app.add_typer(lab_app, name="lab")

    plugin_registry = PluginRegistry()
    for plugin in PluginLoader(EntryPointProvider()).load():
        plugin_registry.register(plugin)

    register_plugin_commands(
        app,
        list_plugins=ListPluginsUseCase(plugin_registry),
        create_plugin=CreatePluginUseCase(
            FilesystemPluginScaffolding(
                plugins_root=root,
                plugin_scaffolds_root=root / "templates" / "plugin",
            )
        ),
    )

    @app.command(
        "legacy",
        context_settings={"allow_extra_args": True, "ignore_unknown_options": True},
        help="Run a pre-migration command while it is being retired.",
    )
    def legacy(context: typer.Context) -> None:
        legacy_main(context.args)

    return app


def main() -> None:
    """Run the installed ``cyberlab`` command."""

    create_app()()


if __name__ == "__main__":
    main()
