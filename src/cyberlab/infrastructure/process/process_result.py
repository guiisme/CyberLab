from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ProcessResult:
    """Result of an executed operating system process."""

    exit_code: int
    stdout: str
    stderr: str
