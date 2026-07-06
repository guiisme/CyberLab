from __future__ import annotations

import typer

from cyberlab.cli.registry import register_commands


def create_app() -> typer.Typer:
    """Create the CyberLab CLI application."""

    app = typer.Typer(
        name="cyberlab",
        help="CyberLab - Reproducible Cybersecurity Labs",
    )

    @app.callback()
    def main() -> None:
        """CyberLab command line interface."""
        pass

    register_commands(app)

    return app
