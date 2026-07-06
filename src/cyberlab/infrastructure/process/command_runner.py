from __future__ import annotations

import subprocess

from cyberlab.domain.models.process_result import ProcessResult


class CommandRunner:
    """Execute operating system commands."""

    def run(
        self,
        command: list[str],
        *,
        timeout: float | None = None,
    ) -> ProcessResult:
        try:
            completed = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
            )
        except FileNotFoundError as exc:
            return ProcessResult(
                exit_code=127,
                stdout="",
                stderr=str(exc),
            )

        return ProcessResult(
            exit_code=completed.returncode,
            stdout=completed.stdout.strip(),
            stderr=completed.stderr.strip(),
        )
