from __future__ import annotations

import pytest

from cyberlab.application.use_cases.stop_lab_use_case import (
    LabStopUseCase,
)
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
        message="Laboratory stopped successfully.",
    )


def test_execute_returns_execution_report() -> None:
    # Arrange
    report = _create_report()

    runner = FakeLabRunner(
        run_reports={},
        stop_reports={
            "xss-basic": report,
        },
    )

    use_case = LabStopUseCase(
        runner,
    )

    # Act
    result = use_case.execute(
        "xss-basic",
    )

    # Assert
    assert result == report


def test_execute_records_stopped_lab_id() -> None:
    # Arrange
    report = _create_report()

    runner = FakeLabRunner(
        run_reports={},
        stop_reports={
            "xss-basic": report,
        },
    )

    use_case = LabStopUseCase(
        runner,
    )

    # Act
    use_case.execute(
        "xss-basic",
    )

    # Assert
    assert runner.stopped_lab_ids == [
        "xss-basic",
    ]


def test_execute_propagates_runner_error() -> None:
    # Arrange
    runner = FakeLabRunner(
        run_reports={},
        stop_reports={},
    )

    use_case = LabStopUseCase(
        runner,
    )

    # Act / Assert
    with pytest.raises(
        AssertionError,
        match="Unexpected lab id: unknown",
    ):
        use_case.execute(
            "unknown",
        )
