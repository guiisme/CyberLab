from typer import Typer

from cyberlab.cli.app import create_app


def test_create_app_returns_typer() -> None:
    app = create_app()

    assert isinstance(app, Typer)
