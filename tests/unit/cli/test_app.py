from typer.testing import CliRunner

from cyberlab.cli.app import create_app
from tests.fakes.fake_command_runner import FakeCommandRunner

runner = CliRunner()


def test_root_help_displays_available_commands() -> None:
    app = create_app(FakeCommandRunner({}))

    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "doctor" in result.stdout
    assert "version" in result.stdout
    assert "lab" in result.stdout
