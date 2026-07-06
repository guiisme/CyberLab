import pytest

from cyberlab.domain.models.lab_manifest import LabManifest
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


def load(
    self,
    lab_id: str,
) -> LabManifest:
    self.loaded_lab_ids.append(lab_id)

    if lab_id not in self._manifests:
        raise AssertionError(f"Unexpected lab id: {lab_id}")

    return self._manifests[lab_id]
