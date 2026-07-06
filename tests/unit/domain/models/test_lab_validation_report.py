from dataclasses import FrozenInstanceError

import pytest

from cyberlab.domain.models.check_result import CheckResult
from cyberlab.domain.models.lab_validation_report import (
    LabValidationReport,
)


def test_report_is_successful_when_all_checks_pass() -> None:
    report = LabValidationReport(
        checks=(
            CheckResult(
                name="lab.yaml",
                success=True,
                message="Found",
            ),
            CheckResult(
                name="README.md",
                success=True,
                message="Found",
            ),
        )
    )

    assert report.success is True


def test_report_is_unsuccessful_when_any_check_fails() -> None:
    report = LabValidationReport(
        checks=(
            CheckResult(
                name="lab.yaml",
                success=True,
                message="Found",
            ),
            CheckResult(
                name="README.md",
                success=False,
                message="Missing",
            ),
        )
    )

    assert report.success is False


def test_report_counts_checks() -> None:
    report = LabValidationReport(
        checks=(
            CheckResult(
                name="lab.yaml",
                success=True,
                message="Found",
            ),
            CheckResult(
                name="README.md",
                success=False,
                message="Missing",
            ),
            CheckResult(
                name="compose.yaml",
                success=True,
                message="Found",
            ),
        )
    )

    assert report.total_checks == 3
    assert report.successful_checks == 2
    assert report.failed_checks == 1


def test_report_is_immutable() -> None:
    report = LabValidationReport(checks=())

    with pytest.raises(FrozenInstanceError):
        report.checks = ()
