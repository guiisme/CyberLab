from __future__ import annotations

from pathlib import Path

from cyberlab.domain.models.process_result import (
    ProcessResult,
)
from cyberlab.infrastructure.docker.docker_compose_lab_lifecycle import (
    DockerComposeLabRunner,
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


def test_run_starts_compose_file() -> None:
    compose_file = "labs/xss-basic/compose.yaml"

    command_runner = FakeCommandRunner(
        responses={
            (
                "docker",
                "compose",
                "-f",
                compose_file,
                "up",
                "-d",
            ): _success_result(),
        },
    )

    service = DockerComposeService(
        command_runner,
    )

    runner = DockerComposeLabRunner(
        compose_service=service,
        labs_root=Path("labs"),
    )

    runner.run("xss-basic")

    assert command_runner.commands == [
        (
            "docker",
            "compose",
            "-f",
            compose_file,
            "up",
            "-d",
        ),
    ]


def test_run_returns_success_report() -> None:
    compose_file = "labs/xss-basic/compose.yaml"

    command_runner = FakeCommandRunner(
        responses={
            (
                "docker",
                "compose",
                "-f",
                compose_file,
                "up",
                "-d",
            ): _success_result(),
        },
    )

    service = DockerComposeService(
        command_runner,
    )

    runner = DockerComposeLabRunner(
        compose_service=service,
        labs_root=Path("labs"),
    )

    report = runner.run("xss-basic")

    assert report.lab_id == "xss-basic"
    assert report.success is True
    assert report.message == "Laboratory started successfully."


def test_run_returns_failure_report() -> None:
    compose_file = "labs/xss-basic/compose.yaml"

    command_runner = FakeCommandRunner(
        responses={
            (
                "docker",
                "compose",
                "-f",
                compose_file,
                "up",
                "-d",
            ): ProcessResult(
                exit_code=1,
                stdout="",
                stderr="Docker failed",
            ),
        },
    )

    service = DockerComposeService(
        command_runner,
    )

    runner = DockerComposeLabRunner(
        compose_service=service,
        labs_root=Path("labs"),
    )

    report = runner.run("xss-basic")

    assert report.lab_id == "xss-basic"
    assert report.success is False
    assert report.message == "Docker failed"


def test_stop_stops_compose_file() -> None:
    compose_file = "labs/xss-basic/compose.yaml"

    command_runner = FakeCommandRunner(
        responses={
            (
                "docker",
                "compose",
                "-f",
                compose_file,
                "down",
            ): _success_result(),
        },
    )

    service = DockerComposeService(
        command_runner,
    )

    runner = DockerComposeLabRunner(
        compose_service=service,
        labs_root=Path("labs"),
    )

    runner.stop("xss-basic")

    assert command_runner.commands == [
        (
            "docker",
            "compose",
            "-f",
            compose_file,
            "down",
        ),
    ]


def test_stop_returns_success_report() -> None:
    compose_file = "labs/xss-basic/compose.yaml"

    command_runner = FakeCommandRunner(
        responses={
            (
                "docker",
                "compose",
                "-f",
                compose_file,
                "down",
            ): _success_result(),
        },
    )

    service = DockerComposeService(
        command_runner,
    )

    runner = DockerComposeLabRunner(
        compose_service=service,
        labs_root=Path("labs"),
    )

    report = runner.stop("xss-basic")

    assert report.lab_id == "xss-basic"
    assert report.success is True
    assert report.message == "Laboratory stopped successfully."


def test_stop_returns_failure_report() -> None:
    compose_file = "labs/xss-basic/compose.yaml"

    command_runner = FakeCommandRunner(
        responses={
            (
                "docker",
                "compose",
                "-f",
                compose_file,
                "down",
            ): ProcessResult(
                exit_code=1,
                stdout="",
                stderr="Docker failed",
            ),
        },
    )

    service = DockerComposeService(
        command_runner,
    )

    runner = DockerComposeLabRunner(
        compose_service=service,
        labs_root=Path("labs"),
    )

    report = runner.stop("xss-basic")

    assert report.lab_id == "xss-basic"
    assert report.success is False
    assert report.message == "Docker failed"
