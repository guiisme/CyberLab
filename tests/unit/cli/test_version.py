from typer.testing import CliRunner

from cyberlab.cli.app import create_app

runner = CliRunner()


def test_version_command_returns_success() -> None:
    result = runner.invoke(create_app(), ["version"])

    assert result.exit_code == 0


def test_version_command_outputs_version() -> None:
    result = runner.invoke(create_app(), ["version"])

    assert result.output.strip() != ""
