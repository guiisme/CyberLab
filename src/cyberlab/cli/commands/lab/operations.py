"""Typer commands for engine-specific laboratory operations."""

from __future__ import annotations

from collections.abc import Callable

import typer

from cyberlab.application.interfaces.lab_operations_protocol import LabOperationsProtocol


def _invoke(operation: Callable[[], object]) -> object:
    try:
        return operation()
    except NotImplementedError as error:
        typer.secho(str(error), fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from error


def register_operations_commands(app: typer.Typer, operations: LabOperationsProtocol) -> None:
    """Register commands delegated to the engine selected by ``lab.yaml``."""

    @app.command("deploy")
    def deploy(lab_id: str) -> None:
        """Deploy a laboratory using its configured engine."""

        typer.echo(_invoke(lambda: operations.deploy(lab_id)))

    @app.command("exec")
    def execute(
        lab_id: str,
        command: str | None = typer.Option(None, "--command", "-c"),
        shell: str = typer.Option("/bin/bash", "--shell"),
    ) -> None:
        """Open a console, or execute a command with --command."""

        if command is not None:
            typer.echo(_invoke(lambda: operations.exec(lab_id, command)))
            return
        typer.echo(_invoke(lambda: operations.console(lab_id, shell)))

    @app.command("submit")
    def submit(
        lab_id: str,
        flag: str = typer.Option(..., "--flag"),
    ) -> None:
        """Submit a challenge flag for validation."""

        if _invoke(lambda: operations.submit(lab_id, flag)):
            typer.secho("Flag correta! Lab concluído.", fg=typer.colors.GREEN)
            return
        typer.secho("Flag incorreta ou indisponível.", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)

    @app.command("proxy")
    def proxy(lab_id: str) -> None:
        """Forward the laboratory service to the local machine."""

        endpoint = _invoke(lambda: operations.proxy(lab_id))
        if endpoint is not None:
            typer.echo(endpoint)

    @app.command("harden")
    def harden(lab_id: str) -> None:
        """Apply the laboratory hardening manifest."""

        typer.echo(_invoke(lambda: operations.harden(lab_id)))

    @app.command("setup-ctf")
    def setup_ctf(lab_id: str, target: str) -> None:
        """Configure CTF artifacts in a target workload."""

        typer.echo(_invoke(lambda: operations.setup_ctf(lab_id, target)))
