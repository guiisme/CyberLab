from dataclasses import FrozenInstanceError

import pytest

from cyberlab.domain.models.check_result import CheckResult


def test_check_result_creation() -> None:
    result = CheckResult(
        name="Docker",
        success=True,
        message="Docker is installed.",
    )

    assert result.name == "Docker"
    assert result.success is True
    assert result.message == "Docker is installed."


def test_check_result_is_immutable() -> None:
    result = CheckResult(
        name="Git",
        success=True,
        message="Git is installed.",
    )

    with pytest.raises(FrozenInstanceError):
        result.name = "Python"  # type: ignore[misc]
