from __future__ import annotations

from dataclasses import dataclass

from cyberlab.domain.models.check_result import CheckResult


@dataclass(frozen=True, slots=True)
class DoctorReport:
    """Represents the result of an environment validation."""

    checks: tuple[CheckResult, ...]

    @property
    def success(self) -> bool:
        return all(check.success for check in self.checks)

    @property
    def total_checks(self) -> int:
        return len(self.checks)

    @property
    def successful_checks(self) -> int:
        return sum(check.success for check in self.checks)

    @property
    def failed_checks(self) -> int:
        return sum(not check.success for check in self.checks)
