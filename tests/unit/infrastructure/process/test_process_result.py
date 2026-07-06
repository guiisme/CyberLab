from dataclasses import FrozenInstanceError

import pytest

from cyberlab.domain.models.process_result import ProcessResult


def test_process_result_creation() -> None:
    result = ProcessResult(
        exit_code=0,
        stdout="git version 2.49.0",
        stderr="",
    )

    assert result.exit_code == 0
    assert result.stdout == "git version 2.49.0"
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
    left = ProcessResult(
        exit_code=0,
        stdout="ok",
        stderr="",
    )

    right = ProcessResult(
        exit_code=0,
        stdout="ok",
        stderr="",
    )

    assert left == right
