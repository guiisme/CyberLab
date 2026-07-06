from cyberlab.application.use_cases.doctor_use_case import DoctorUseCase
from cyberlab.domain.models.process_result import ProcessResult
from tests.fakes.fake_command_runner import FakeCommandRunner


def test_execute_returns_successful_report() -> None:
    # Arrange
    runner = FakeCommandRunner(
        {
            ("git", "--version"): ProcessResult(
                exit_code=0,
                stdout="git version 2.49.0",
                stderr="",
            ),
            ("docker", "--version"): ProcessResult(
                exit_code=0,
                stdout="Docker version 28.0.0",
                stderr="",
            ),
            ("python", "--version"): ProcessResult(
                exit_code=0,
                stdout="Python 3.12.3",
                stderr="",
            ),
            ("uv", "--version"): ProcessResult(
                exit_code=0,
                stdout="uv 0.8.0",
                stderr="",
            ),
        }
    )

    doctor = DoctorUseCase(runner)

    # Act
    report = doctor.execute()

    # Assert
    assert report.success is True
    assert report.total_checks == 4
    assert report.successful_checks == 4
    assert report.failed_checks == 0

    assert all(check.success for check in report.checks)


def test_execute_returns_failed_report_when_docker_is_missing() -> None:
    # Arrange
    runner = FakeCommandRunner(
        {
            ("git", "--version"): ProcessResult(
                exit_code=0,
                stdout="git version 2.49.0",
                stderr="",
            ),
            ("docker", "--version"): ProcessResult(
                exit_code=127,
                stdout="",
                stderr="docker: command not found",
            ),
            ("python", "--version"): ProcessResult(
                exit_code=0,
                stdout="Python 3.12.3",
                stderr="",
            ),
            ("uv", "--version"): ProcessResult(
                exit_code=0,
                stdout="uv 0.8.0",
                stderr="",
            ),
        }
    )

    doctor = DoctorUseCase(runner)

    # Act
    report = doctor.execute()

    # Assert
    assert report.success is False
    assert report.total_checks == 4
    assert report.successful_checks == 3
    assert report.failed_checks == 1

    docker_check = report.checks[1]

    assert docker_check.name == "Docker"
    assert docker_check.success is False
    assert docker_check.message == "docker: command not found"


def test_execute_runs_commands_in_expected_order() -> None:
    # Arrange
    runner = FakeCommandRunner(
        {
            ("git", "--version"): ProcessResult(0, "", ""),
            ("docker", "--version"): ProcessResult(0, "", ""),
            ("python", "--version"): ProcessResult(0, "", ""),
            ("uv", "--version"): ProcessResult(0, "", ""),
        }
    )

    doctor = DoctorUseCase(runner)

    # Act
    doctor.execute()

    # Assert
    assert runner.commands == [
        ("git", "--version"),
        ("docker", "--version"),
        ("python", "--version"),
        ("uv", "--version"),
    ]
