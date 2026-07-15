from pathlib import Path
from unittest.mock import MagicMock, patch

from src.cyberlab_plugin_podman.infrastructure.podman_compose import PodmanComposeLabLifecycle
from src.cyberlab_plugin_podman.plugin import Podman


def test_run_executes_podman_compose_up():
    lifecycle = PodmanComposeLabLifecycle()
    lab_path = Path("/tmp/fake-lab")

    with patch("subprocess.run") as mock_run:
        lifecycle.run(lab_path)
        mock_run.assert_called_once_with(["podman-compose", "up", "-d"], cwd=lab_path, check=True)


def test_stop_executes_podman_compose_down():
    lifecycle = PodmanComposeLabLifecycle()
    lab_path = Path("/tmp/fake-lab")

    with patch("subprocess.run") as mock_run:
        lifecycle.stop(lab_path)
        mock_run.assert_called_once_with(["podman-compose", "down"], cwd=lab_path, check=True)


def test_status_executes_podman_compose_ps_and_returns_output():
    lifecycle = PodmanComposeLabLifecycle()
    lab_path = Path("/tmp/fake-lab")

    with patch("subprocess.run") as mock_run:
        mock_process = MagicMock()
        mock_process.stdout = "Up 2 hours"
        mock_run.return_value = mock_process

        result = lifecycle.status(lab_path)

        mock_run.assert_called_once_with(
            ["podman-compose", "ps"], cwd=lab_path, capture_output=True, text=True, check=True
        )
        assert result == "Up 2 hours"


def test_restart_executes_podman_compose_restart():
    lifecycle = PodmanComposeLabLifecycle()
    lab_path = Path("/tmp/fake-lab")

    with patch("subprocess.run") as mock_run:
        lifecycle.restart(lab_path)
        mock_run.assert_called_once_with(["podman-compose", "restart"], cwd=lab_path, check=True)


def test_logs_executes_podman_compose_logs():
    lifecycle = PodmanComposeLabLifecycle()
    lab_path = Path("/tmp/fake-lab")

    with patch("subprocess.run") as mock_run:
        lifecycle.logs(lab_path)
        mock_run.assert_called_once_with(["podman-compose", "logs"], cwd=lab_path, check=True)


def test_logs_with_follow_and_tail_flags():
    lifecycle = PodmanComposeLabLifecycle()
    lab_path = Path("/tmp/fake-lab")

    with patch("subprocess.run") as mock_run:
        lifecycle.logs(lab_path, follow=True, tail=True)
        mock_run.assert_called_once_with(
            ["podman-compose", "logs", "--follow", "--tail=all"], cwd=lab_path, check=True
        )


def test_plugin_manifest_contains_correct_metadata():
    plugin = Podman()
    manifest = plugin.manifest

    assert manifest.id == "podman"
    assert manifest.name == "Podman Execution Adapter"
    assert manifest.version == "0.1.0"


def test_plugin_instantiates_lifecycle_adapter():
    plugin = Podman()
    assert isinstance(plugin._lifecycle, PodmanComposeLabLifecycle)
