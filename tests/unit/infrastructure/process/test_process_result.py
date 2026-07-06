from dataclasses import FrozenInstanceError

import pytest

from cyberlab.infrastructure.process.process_result import ProcessResult


def test_process_result_creation() -> None:
    result = ProcessResult(
        exit_code=0,
        stdout="ok",
        stderr="",
    )

    assert result.exit_code == 0
    assert result.stdout == "ok"
    assert result.stderr == ""


def test_process_result_is_immutable() -> None:
    result = ProcessResult(
        exit_code=0,
        stdout="ok",
        stderr="",
    )

    with pytest.raises(FrozenInstanceError):
        result.exit_code = 1  # type: ignore[misc]


def test_process_result_equality() -> None:
    left = ProcessResult(0, "ok", "")
    right = ProcessResult(0, "ok", "")

    assert left == right
