from __future__ import annotations

from pathlib import Path

from cyberlab.domain.models.process_result import (
    ProcessResult,
)
from cyberlab.infrastructure.docker.docker_compose_service import (
    DockerComposeService,
)
from tests.fakes.fake_command_runner import (
    FakeCommandRunner,
)


def _success_result() -> ProcessResult:
    return ProcessResult(
        exit_code=0,
        stdout="Started",
        stderr="",
    )


def _failure_result() -> ProcessResult:
    return ProcessResult(
        exit_code=1,
        stdout="",
        stderr="Docker failed",
    )


#
# UP
#


def test_up_executes_docker_compose_command() -> None:
    compose_file = Path("labs/xss-basic/compose.yaml")

    expected = _success_result()

    command_runner = FakeCommandRunner(
        responses={
            (
                "docker",
                "compose",
                "-f",
                str(compose_file),
                "up",
                "-d",
            ): expected,
        },
    )

    service = DockerComposeService(
        command_runner=command_runner,
    )

    result = service.up(compose_file)

    assert result == expected

    assert command_runner.commands == [
        (
            "docker",
            "compose",
            "-f",
            str(compose_file),
            "up",
            "-d",
        ),
    ]


def test_up_returns_process_failure() -> None:
    compose_file = Path("labs/xss-basic/compose.yaml")

    expected = _failure_result()

    command_runner = FakeCommandRunner(
        responses={
            (
                "docker",
                "compose",
                "-f",
                str(compose_file),
                "up",
                "-d",
            ): expected,
        },
    )

    service = DockerComposeService(
        command_runner=command_runner,
    )

    result = service.up(compose_file)

    assert result.exit_code == 1
    assert result.stderr == "Docker failed"


#
# DOWN
#


def test_down_executes_docker_compose_command() -> None:
    compose_file = Path("labs/xss-basic/compose.yaml")

    expected = _success_result()

    command_runner = FakeCommandRunner(
        responses={
            (
                "docker",
                "compose",
                "-f",
                str(compose_file),
                "down",
            ): expected,
        },
    )

    service = DockerComposeService(
        command_runner=command_runner,
    )

    result = service.down(
        compose_file,
    )

    assert result == expected

    assert command_runner.commands == [
        (
            "docker",
            "compose",
            "-f",
            str(compose_file),
            "down",
        ),
    ]


def test_down_returns_process_result() -> None:
    compose_file = Path("labs/xss-basic/compose.yaml")

    expected = _success_result()

    command_runner = FakeCommandRunner(
        responses={
            (
                "docker",
                "compose",
                "-f",
                str(compose_file),
                "down",
            ): expected,
        },
    )

    service = DockerComposeService(
        command_runner=command_runner,
    )

    result = service.down(
        compose_file,
    )

    assert result == expected


def test_down_returns_process_failure() -> None:
    compose_file = Path("labs/xss-basic/compose.yaml")

    expected = _failure_result()

    command_runner = FakeCommandRunner(
        responses={
            (
                "docker",
                "compose",
                "-f",
                str(compose_file),
                "down",
            ): expected,
        },
    )

    service = DockerComposeService(
        command_runner=command_runner,
    )

    result = service.down(
        compose_file,
    )

    assert result.exit_code == 1
    assert result.stderr == "Docker failed"


#
# Logs
#


def test_logs_executes_docker_compose_command() -> None:
    compose_file = Path("labs/xss-basic/compose.yaml")

    expected = _success_result()

    command_runner = FakeCommandRunner(
        responses={
            (
                "docker",
                "compose",
                "-f",
                str(compose_file),
                "logs",
            ): expected,
        },
    )

    service = DockerComposeService(
        command_runner=command_runner,
    )

    result = service.logs(compose_file)

    assert result == expected

    assert command_runner.commands == [
        (
            "docker",
            "compose",
            "-f",
            str(compose_file),
            "logs",
        ),
    ]


def test_logs_returns_process_failure() -> None:
    compose_file = Path("labs/xss-basic/compose.yaml")

    expected = _failure_result()

    command_runner = FakeCommandRunner(
        responses={
            (
                "docker",
                "compose",
                "-f",
                str(compose_file),
                "logs",
            ): expected,
        },
    )

    service = DockerComposeService(
        command_runner=command_runner,
    )

    result = service.logs(compose_file)

    assert result.exit_code == 1
    assert result.stderr == "Docker failed"
