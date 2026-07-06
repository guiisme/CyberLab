from __future__ import annotations

from dataclasses import dataclass

from cyberlab.domain.models.check_result import CheckResult


@dataclass(frozen=True, slots=True)
class LabValidationReport:
    """Result of a laboratory validation."""

    checks: tuple[CheckResult, ...]

    @property
    def success(self) -> bool:
        """Return True when all validation checks succeeded."""
        return all(check.success for check in self.checks)

    @property
    def total_checks(self) -> int:
        """Return the total number of validation checks."""
        return len(self.checks)

    @property
    def successful_checks(self) -> int:
        """Return the number of successful validation checks."""
        return sum(check.success for check in self.checks)

    @property
    def failed_checks(self) -> int:
        """Return the number of failed validation checks."""
        return self.total_checks - self.successful_checks
