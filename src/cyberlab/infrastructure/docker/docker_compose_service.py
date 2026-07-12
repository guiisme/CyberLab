from __future__ import annotations

from pathlib import Path

from cyberlab.application.interfaces.command_runner_protocol import (
    CommandRunnerProtocol,
)
from cyberlab.domain.models.process_result import (
    ProcessResult,
)


class DockerComposeService:
    """Execute Docker Compose commands."""

    def __init__(
        self,
        command_runner: CommandRunnerProtocol,
    ) -> None:
        self._command_runner = command_runner

    def up(
        self,
        compose_file: Path,
    ) -> ProcessResult:
        """Start a Docker Compose environment."""

        return self._command_runner.run(
            [
                "docker",
                "compose",
                "-f",
                str(compose_file),
                "up",
                "-d",
            ]
        )

    def down(
        self,
        compose_file: Path,
    ) -> ProcessResult:
        """Stop a Docker Compose environment."""

        return self._command_runner.run(
            [
                "docker",
                "compose",
                "-f",
                str(compose_file),
                "down",
            ]
        )

    def ps(
        self,
        compose_file: Path,
    ) -> ProcessResult:
        """Show the status of a Docker Compose environment."""

        return self._command_runner.run(
            [
                "docker",
                "compose",
                "-f",
                str(compose_file),
                "ps",
            ]
        )

    def restart(
        self,
        compose_file: Path,
    ) -> ProcessResult:
        """Restart a Docker Compose environment."""

        return self._command_runner.run(
            [
                "docker",
                "compose",
                "-f",
                str(compose_file),
                "restart",
            ]
        )

    def logs(
        self,
        compose_file: Path,
    ) -> ProcessResult:
        """Show logs for a Docker Compose environment."""

        return self._command_runner.run(
            [
                "docker",
                "compose",
                "-f",
                str(compose_file),
                "logs",
            ]
        )
