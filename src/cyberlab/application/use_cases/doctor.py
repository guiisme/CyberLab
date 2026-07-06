from __future__ import annotations

from cyberlab.application.interfaces.command_runner_protocol import (
    CommandRunnerProtocol,
)
from cyberlab.domain.models.check_result import CheckResult
from cyberlab.domain.models.doctor_report import DoctorReport


class DoctorUseCase:
    """Validate the local environment required by CyberLab."""

    def __init__(self, runner: CommandRunnerProtocol) -> None:
        self._runner = runner

    def execute(self) -> DoctorReport:
        """Run all environment checks."""

        checks = (
            self._run_check("Git", ["git", "--version"]),
            self._run_check("Docker", ["docker", "--version"]),
            self._run_check("Python", ["python", "--version"]),
            self._run_check("uv", ["uv", "--version"]),
        )

        return DoctorReport(checks=checks)

    def _run_check(
        self,
        name: str,
        command: list[str],
    ) -> CheckResult:
        """Execute a single environment check."""

        result = self._runner.run(command)

        if result.exit_code == 0:
            message = result.stdout
        else:
            message = result.stderr

        return CheckResult(
            name=name,
            success=result.exit_code == 0,
            message=message,
        )
