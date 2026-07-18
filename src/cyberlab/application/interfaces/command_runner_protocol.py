from __future__ import annotations

from typing import Protocol

from cyberlab.domain.models.process_result import ProcessResult


class CommandRunnerProtocol(Protocol):
    """Execute operating system commands."""

    def run(
        self,
        command: list[str],
        *,
        timeout: float | None = None,
    ) -> ProcessResult: ...

    def run_interactive(self, command: list[str]) -> int: ...
