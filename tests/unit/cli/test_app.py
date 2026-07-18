from pathlib import Path

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


def test_lab_help_displays_engine_operations() -> None:
    app = create_app(FakeCommandRunner({}))

    result = runner.invoke(app, ["lab", "--help"])

    assert result.exit_code == 0
    assert "deploy" in result.stdout
    assert "exec" in result.stdout
    assert "submit" in result.stdout
    assert "proxy" in result.stdout
    assert "harden" in result.stdout


def test_lab_create_supports_kali_template(tmp_path: Path) -> None:
    app = create_app(FakeCommandRunner({}), labs_root=tmp_path)

    result = runner.invoke(
        app,
        ["lab", "create", "kali-pentest", "--template", "kali", "--profile", "web"],
    )

    assert result.exit_code == 0
    assert (tmp_path / "kali-pentest" / "Dockerfile").is_file()
    assert "KALI_PROFILE=web" in (tmp_path / "kali-pentest" / "Dockerfile").read_text(
        encoding="utf-8"
    )
