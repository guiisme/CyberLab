import subprocess
from unittest.mock import MagicMock, patch

import pytest

from cyberlab.sdk import LabExecutionError, LaboratoryState
from cyberlab_plugin_podman.infrastructure.podman_compose import PodmanComposeLabLifecycle
from cyberlab_plugin_podman.plugin import PodmanPlugin


def test_plugin_manifest_contains_correct_metadata():
    plugin = PodmanPlugin()

    assert plugin.manifest.id == "podman"
    assert plugin.manifest.name == "Podman Execution Adapter"
    assert plugin.manifest.version == "0.1.0"


def test_plugin_instantiates_lifecycle_adapter():
    plugin = PodmanPlugin()

    assert isinstance(plugin._lifecycle, PodmanComposeLabLifecycle)
    assert plugin.get_lifecycle_adapter() is plugin._lifecycle


def test_run_executes_podman_compose_up():
    lifecycle = PodmanComposeLabLifecycle()

    with patch("subprocess.run") as mock_run:
        lifecycle.run("example")
        mock_run.assert_called_once_with(
            [
                "podman-compose",
                "-f",
                str(lifecycle._resolve_path("example") / "docker-compose.yml"),
                "up",
                "-d",
            ],
            cwd=lifecycle._resolve_path("example"),
            capture_output=True,
            text=True,
            check=True,
        )


def test_run_translates_process_errors_to_domain_errors():
    lifecycle = PodmanComposeLabLifecycle()

    with patch(
        "subprocess.run",
        side_effect=subprocess.CalledProcessError(1, "podman-compose", stderr="container failed"),
    ):
        with pytest.raises(
            LabExecutionError, match="Podman Compose up -d failed: container failed"
        ):
            lifecycle.run("example")


def test_status_translates_podman_output_to_domain_state():
    lifecycle = PodmanComposeLabLifecycle()

    with patch("subprocess.run", return_value=MagicMock(stdout="web  Up 2 minutes")):
        status = lifecycle.status("example")

    assert status.state is LaboratoryState.RUNNING
