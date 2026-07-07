from __future__ import annotations

from cyberlab.infrastructure.runner.noop_lab_runner import (
    NoOpLabRunner,
)


def test_run_returns_successful_execution_report() -> None:
    # Arrange
    runner = NoOpLabRunner()

    # Act
    report = runner.run("xss-basic")

    # Assert
    assert report.lab_id == "xss-basic"
    assert report.success is True
    assert report.message == "Laboratory started successfully."
