from __future__ import annotations

from cyberlab.application.interfaces.command_runner_protocol import (
    CommandRunnerProtocol,
)
from cyberlab.domain.models.process_result import ProcessResult


class FakeCommandRunner(CommandRunnerProtocol):
    """In-memory implementation of CommandRunnerProtocol for tests."""

    def __init__(
        self,
        responses: dict[tuple[str, ...], ProcessResult],
    ) -> None:
        self._responses = responses

    def run(
        self,
        command: list[str],
        *,
        timeout: float | None = None,
    ) -> ProcessResult:
        key = tuple(command)

        if key not in self._responses:
            raise AssertionError(f"Unexpected command: {command}")

        return self._responses[key]
