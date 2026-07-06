import pytest

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
        ),
    )


def test_validate_returns_report() -> None:
    # Arrange
    report = _create_report()

    validator = FakeLabValidator(
        {
            "xss-basic": report,
        }
    )

    # Act
    result = validator.validate("xss-basic")

    # Assert
    assert result == report


def test_validate_records_requested_lab_id() -> None:
    # Arrange
    report = _create_report()

    validator = FakeLabValidator(
        {
            "xss-basic": report,
        }
    )

    # Act
    validator.validate("xss-basic")

    # Assert
    assert validator.requested_lab_ids == [
        "xss-basic",
    ]


def test_validate_raises_assertion_error_for_unknown_lab() -> None:
    # Arrange
    validator = FakeLabValidator({})

    # Act / Assert
    with pytest.raises(
        AssertionError,
        match="Unexpected lab id: unknown",
    ):
        validator.validate("unknown")
