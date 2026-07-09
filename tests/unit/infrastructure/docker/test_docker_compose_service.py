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


def test_up_executes_docker_compose_command() -> None:
    compose_file = Path("labs/xss-basic/compose.yaml")

    expected = ProcessResult(
        exit_code=0,
        stdout="Started",
        stderr="",
    )

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
        }
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
            "labs/xss-basic/compose.yaml",
            "up",
            "-d",
        )
    ]


def test_up_returns_process_failure() -> None:
    compose_file = Path("labs/xss-basic/compose.yaml")

    expected = ProcessResult(
        exit_code=1,
        stdout="",
        stderr="Docker failed",
    )

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
        }
    )

    service = DockerComposeService(
        command_runner=command_runner,
    )

    result = service.up(compose_file)

    assert result.exit_code == 1
    assert result.stderr == "Docker failed"
