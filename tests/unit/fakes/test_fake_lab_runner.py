from __future__ import annotations

import pytest

from cyberlab.domain.models.lab_execution_report import (
    LabExecutionReport,
)
from tests.fakes.fake_lab_runner import (
    FakeLabRunner,
)


def _create_report() -> LabExecutionReport:
    return LabExecutionReport(
        lab_id="xss-basic",
        success=True,
        message="Laboratory started successfully.",
    )


def test_run_returns_execution_report() -> None:
    # Arrange
    report = _create_report()

    runner = FakeLabRunner(
        {
            "xss-basic": report,
        }
    )

    # Act
    result = runner.run("xss-basic")

    # Assert
    assert result == report


def test_run_records_requested_lab_id() -> None:
    # Arrange
    report = _create_report()

    runner = FakeLabRunner(
        {
            "xss-basic": report,
        }
    )

    # Act
    runner.run("xss-basic")

    # Assert
    assert runner.requested_lab_ids == [
        "xss-basic",
    ]


def test_run_raises_assertion_error_for_unknown_lab() -> None:
    # Arrange
    runner = FakeLabRunner({})

    # Act / Assert
    with pytest.raises(
        AssertionError,
        match="Unexpected lab id: unknown",
    ):
        runner.run("unknown")
