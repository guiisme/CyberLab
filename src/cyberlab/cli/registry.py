from __future__ import annotations

import typer

from cyberlab.cli.commands.version import register as register_version


def register_commands(app: typer.Typer) -> None:
    """Register all CLI commands."""

    register_version(app)
