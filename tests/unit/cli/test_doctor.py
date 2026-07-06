from typer.testing import CliRunner

from cyberlab.cli.app import create_app
from cyberlab.domain.models.process_result import ProcessResult
from tests.fakes.fake_command_runner import FakeCommandRunner

runner = CliRunner()


def test_doctor_returns_success() -> None:
    # Arrange
    fake_runner = FakeCommandRunner(
        {
            ("git", "--version"): ProcessResult(0, "git version", ""),
            ("docker", "--version"): ProcessResult(0, "Docker version", ""),
            ("python", "--version"): ProcessResult(0, "Python 3.12.3", ""),
            ("uv", "--version"): ProcessResult(0, "uv 0.8.0", ""),
        }
    )

    app = create_app(fake_runner)

    # Act
    result = runner.invoke(app, ["doctor"])

    # Assert
    assert result.exit_code == 0

    assert "[OK] Git" in result.stdout
    assert "[OK] Docker" in result.stdout
    assert "[OK] Python" in result.stdout
    assert "[OK] uv" in result.stdout


def test_doctor_returns_failure() -> None:
    # Arrange
    fake_runner = FakeCommandRunner(
        {
            ("git", "--version"): ProcessResult(0, "git version", ""),
            ("docker", "--version"): ProcessResult(
                127,
                "",
                "docker not found",
            ),
            ("python", "--version"): ProcessResult(0, "Python 3.12.3", ""),
            ("uv", "--version"): ProcessResult(0, "uv 0.8.0", ""),
        }
    )

    app = create_app(fake_runner)

    # Act
    result = runner.invoke(app, ["doctor"])

    # Assert
    assert result.exit_code == 1

    assert "[FAIL] Docker" in result.stdout
