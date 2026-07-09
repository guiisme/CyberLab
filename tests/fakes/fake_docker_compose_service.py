from __future__ import annotations

from pathlib import Path

from cyberlab.domain.models.process_result import (
    ProcessResult,
)


class FakeDockerComposeService:
    """In-memory Docker Compose service."""

    def __init__(
        self,
        result: ProcessResult,
    ) -> None:
        self._result = result
        self.compose_files: list[Path] = []

    def up(
        self,
        compose_file: Path,
    ) -> ProcessResult:
        self.compose_files.append(compose_file)
        return self._result
