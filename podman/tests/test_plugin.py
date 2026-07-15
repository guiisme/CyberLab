from pathlib import Path
from unittest.mock import patch

from cyberlab_plugin_podman.infrastructure.podman_compose import PodmanComposeLabLifecycle


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
