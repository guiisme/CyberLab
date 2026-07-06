import pytest

from cyberlab.domain.models.process_result import ProcessResult
from tests.fakes.fake_command_runner import FakeCommandRunner


def test_returns_configured_response() -> None:
    expected = ProcessResult(
        exit_code=0,
        stdout="git version 2.49.0",
        stderr="",
    )

    runner = FakeCommandRunner(
        {
            ("git", "--version"): expected,
        }
    )

    result = runner.run(["git", "--version"])

    assert result == expected


def test_raises_for_unexpected_command() -> None:
    runner2 = FakeCommandRunner({})

    with pytest.raises(AssertionError):
        runner2.run(["docker", "--version"])
