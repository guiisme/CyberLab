from dataclasses import FrozenInstanceError

import pytest

from cyberlab.domain.models.check_result import CheckResult
from cyberlab.domain.models.doctor_report import DoctorReport


def test_doctor_report_creation() -> None:
    report = DoctorReport(
        checks=(
            CheckResult(
                name="Git",
                success=True,
                message="Installed",
            ),
        ),
    )

    assert len(report.checks) == 1


def test_report_success_when_all_checks_pass() -> None:
    report = DoctorReport(
        checks=(
            CheckResult("Git", True, "Installed"),
            CheckResult("Docker", True, "Installed"),
        ),
    )

    assert report.success is True


def test_report_failure_when_any_check_fails() -> None:
    report = DoctorReport(
        checks=(
            CheckResult("Git", True, "Installed"),
            CheckResult("Docker", False, "Missing"),
        ),
    )

    assert report.success is False


def test_report_statistics() -> None:
    report = DoctorReport(
        checks=(
            CheckResult("Git", True, ""),
            CheckResult("Docker", False, ""),
            CheckResult("Python", True, ""),
        ),
    )

    assert report.total_checks == 3
    assert report.successful_checks == 2
    assert report.failed_checks == 1


def test_doctor_report_is_immutable() -> None:
    report = DoctorReport(
        checks=(),
    )

    with pytest.raises(FrozenInstanceError):
        report.checks = ()  # type: ignore[misc]
