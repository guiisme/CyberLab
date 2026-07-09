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
        """Start a Docker Compose project."""

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
