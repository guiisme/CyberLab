from pathlib import Path

from cyberlab.domain.models.laboratory_state import LaboratoryState
from cyberlab.domain.models.process_result import ProcessResult
from cyberlab.infrastructure.docker.docker_compose_lab_status import (
    DockerComposeLabStatus,
)
from cyberlab.infrastructure.docker.docker_compose_service import (
    DockerComposeService,
)
from tests.fakes.fake_command_runner import FakeCommandRunner


def test_returns_running_status() -> None:
    compose_file = Path("labs") / "xss-basic" / "compose.yaml"

    runner = FakeCommandRunner(
        {
            (
                "docker",
                "compose",
                "-f",
                str(compose_file),
                "ps",
            ): ProcessResult(
                exit_code=0,
                stdout="Up",
                stderr="",
            ),
        }
    )

    service = DockerComposeService(runner)

    adapter = DockerComposeLabStatus(
        service,
        Path("labs"),
    )

    status = adapter.status("xss-basic")

    assert status.state is LaboratoryState.RUNNING
    assert status.is_running


def test_returns_stopped_status() -> None:
    compose_file = Path("labs") / "xss-basic" / "compose.yaml"

    runner = FakeCommandRunner(
        {
            (
                "docker",
                "compose",
                "-f",
                str(compose_file),
                "ps",
            ): ProcessResult(
                exit_code=0,
                stdout="",
                stderr="",
            ),
        }
    )

    service = DockerComposeService(runner)

    adapter = DockerComposeLabStatus(
        service,
        Path("labs"),
    )

    status = adapter.status("xss-basic")

    assert status.state is LaboratoryState.STOPPED
    assert status.is_stopped


def test_returns_stopped_when_command_fails() -> None:
    compose_file = Path("labs") / "xss-basic" / "compose.yaml"

    runner = FakeCommandRunner(
        {
            (
                "docker",
                "compose",
                "-f",
                str(compose_file),
                "ps",
            ): ProcessResult(
                exit_code=1,
                stdout="",
                stderr="Docker error",
            ),
        }
    )

    service = DockerComposeService(runner)

    adapter = DockerComposeLabStatus(
        service,
        Path("labs"),
    )

    status = adapter.status("xss-basic")

    assert status.state is LaboratoryState.STOPPED
    assert status.is_stopped
