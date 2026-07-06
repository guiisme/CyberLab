from typer.testing import CliRunner

from cyberlab.cli.app import create_app
from cyberlab.shared.version import get_version

runner = CliRunner()


def test_version_command_returns_success() -> None:
    app = create_app()

    result = runner.invoke(app, ["version"])

    assert result.exit_code == 0


def test_version_command_outputs_version() -> None:
    app = create_app()

    result = runner.invoke(app, ["version"])

    assert get_version() in result.stdout
