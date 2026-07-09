from dataclasses import FrozenInstanceError

import pytest

from cyberlab.domain.models.lab_execution_result import (
    LabExecutionResult,
)


def test_should_create_execution_result() -> None:
    result = LabExecutionResult(
        success=True,
        message="Laboratory executed successfully.",
    )

    assert result.success is True
    assert result.message == "Laboratory executed successfully."


def test_should_be_immutable() -> None:
    result = LabExecutionResult(
        success=True,
        message="ok",
    )

    with pytest.raises(FrozenInstanceError):
        result.success = False
