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


#
# Logs
#


def test_logs_executes_docker_compose_command() -> None:
    compose_file = "labs/xss-basic/compose.yaml"

    command_runner = FakeCommandRunner(
        responses={
            (
                "docker",
                "compose",
                "-f",
                compose_file,
                "logs",
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

    runner.logs("xss-basic")

    assert command_runner.commands == [
        (
            "docker",
            "compose",
            "-f",
            compose_file,
            "logs",
        ),
    ]


def test_logs_returns_failure_report() -> None:
    compose_file = "labs/xss-basic/compose.yaml"

    command_runner = FakeCommandRunner(
        responses={
            (
                "docker",
                "compose",
                "-f",
                compose_file,
                "logs",
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

    report = runner.logs("xss-basic")

    assert report.lab_id == "xss-basic"
    assert report.content == "Docker failed"


def test_exec_runs_command_in_first_compose_container() -> None:
    compose_file = "labs/xss-basic/compose.yaml"
    command_runner = FakeCommandRunner(
        responses={
            ("docker", "compose", "-f", compose_file, "ps", "-q"): ProcessResult(
                exit_code=0,
                stdout="container-123\n",
                stderr="",
            ),
            ("docker", "exec", "container-123", "sh", "-c", "id"): ProcessResult(
                exit_code=0,
                stdout="uid=0",
                stderr="",
            ),
        }
    )
    runner = DockerComposeLabRunner(DockerComposeService(command_runner), Path("labs"))

    assert runner.exec("xss-basic", "id") == "uid=0"


def test_exec_reports_missing_compose_container() -> None:
    compose_file = "labs/xss-basic/compose.yaml"
    command_runner = FakeCommandRunner(
        responses={
            ("docker", "compose", "-f", compose_file, "ps", "-q"): ProcessResult(
                exit_code=0,
                stdout="",
                stderr="",
            )
        }
    )
    runner = DockerComposeLabRunner(DockerComposeService(command_runner), Path("labs"))

    assert runner.exec("xss-basic", "id") == (
        "Erro ao executar: nenhum container ativo para 'xss-basic'."
    )


def test_proxy_reports_published_compose_ports() -> None:
    compose_file = "labs/xss-basic/compose.yaml"
    command_runner = FakeCommandRunner(
        responses={
            ("docker", "compose", "-f", compose_file, "ps", "-q"): ProcessResult(
                exit_code=0,
                stdout="container-123\n",
                stderr="",
            ),
            ("docker", "port", "container-123"): ProcessResult(
                exit_code=0,
                stdout="80/tcp -> 127.0.0.1:8080\n",
                stderr="",
            ),
        }
    )
    runner = DockerComposeLabRunner(DockerComposeService(command_runner), Path("labs"))

    assert runner.proxy("xss-basic") == (
        "Endpoint(s) publicado(s) para 'xss-basic':\n80/tcp -> 127.0.0.1:8080"
    )


def test_console_opens_interactive_shell_in_first_compose_container() -> None:
    compose_file = "labs/xss-basic/compose.yaml"
    command_runner = FakeCommandRunner(
        responses={
            ("docker", "compose", "-f", compose_file, "ps", "-q"): ProcessResult(
                exit_code=0,
                stdout="container-123\n",
                stderr="",
            ),
            ("docker", "exec", "-it", "container-123", "/bin/bash"): ProcessResult(
                exit_code=0,
                stdout="",
                stderr="",
            ),
        }
    )
    runner = DockerComposeLabRunner(DockerComposeService(command_runner), Path("labs"))

    assert runner.console("xss-basic") == "Console encerrado."
    assert command_runner.commands[-1] == ("docker", "exec", "-it", "container-123", "/bin/bash")
