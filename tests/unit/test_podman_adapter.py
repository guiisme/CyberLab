# Exemplo rápido para um novo tests/unit/test_podman_adapter.py
from unittest.mock import patch

from podman.src.cyberlab_plugin_podman.infrastructure.podman_compose import (
    PodmanComposeLabLifecycle,
)


def test_run_executes_correct_command():
    adapter = PodmanComposeLabLifecycle()
    with patch("subprocess.run") as mock_run:
        adapter.run("teste-pr019")
        # Verifica se ele chamou o binário correto com o caminho absoluto
        args, _ = mock_run.call_args
        assert "/usr/bin/podman-compose" in args[0][0]
        assert "-f" in args[0]
