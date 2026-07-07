from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from cyberlab.domain.models.lab_execution_report import (
    LabExecutionReport,
)


def test_report_stores_execution_information() -> None:
    # Arrange
    report = LabExecutionReport(
        lab_id="xss-basic",
        success=True,
        message="Laboratory started successfully.",
    )

    # Assert
    assert report.lab_id == "xss-basic"
    assert report.success is True
    assert report.message == "Laboratory started successfully."


def test_report_is_immutable() -> None:
    # Arrange
    report = LabExecutionReport(
        lab_id="xss-basic",
        success=True,
        message="Laboratory started successfully.",
    )

    # Act / Assert
    with pytest.raises(FrozenInstanceError):
        report.lab_id = "csrf-basic"
