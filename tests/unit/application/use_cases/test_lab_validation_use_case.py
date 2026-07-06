from __future__ import annotations

import pytest

from cyberlab.application.use_cases.lab_validation_use_case import (
    LabValidationUseCase,
)
from cyberlab.domain.models.check_result import CheckResult
from cyberlab.domain.models.lab_validation_report import (
    LabValidationReport,
)
from tests.fakes.fake_lab_validator import (
    FakeLabValidator,
)


def _create_report() -> LabValidationReport:
    return LabValidationReport(
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
            CheckResult(
                name="compose.yaml",
                success=True,
                message="Found",
            ),
        )
    )


def test_execute_returns_validation_report() -> None:
    # Arrange
    report = _create_report()

    validator = FakeLabValidator(
        {
            "xss-basic": report,
        }
    )

    use_case = LabValidationUseCase(
        validator,
    )

    # Act
    result = use_case.execute("xss-basic")

    # Assert
    assert result == report


def test_execute_records_requested_lab_id() -> None:
    # Arrange
    report = _create_report()

    validator = FakeLabValidator(
        {
            "xss-basic": report,
        }
    )

    use_case = LabValidationUseCase(
        validator,
    )

    # Act
    use_case.execute("xss-basic")

    # Assert
    assert validator.requested_lab_ids == [
        "xss-basic",
    ]


def test_execute_propagates_validator_error() -> None:
    # Arrange
    validator = FakeLabValidator({})

    use_case = LabValidationUseCase(
        validator,
    )

    # Act / Assert
    with pytest.raises(
        AssertionError,
        match="Unexpected lab id: unknown",
    ):
        use_case.execute("unknown")
