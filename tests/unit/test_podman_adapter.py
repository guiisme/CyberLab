import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from cyberlab_plugin_podman.infrastructure.podman_compose import (
    PodmanComposeLabLifecycle,
)


@patch("subprocess.run")
def test_run_executes_correct_command(mock_run):
    # Arrange
    adapter = PodmanComposeLabLifecycle()
    lab_id = "teste-pr019"

    # Simula o retorno de sucesso do subprocess
    mock_run.return_value = MagicMock(returncode=0, stdout="success")

    # Act
    adapter.run(lab_id)

    # Assert
    # Verifica se chamou exatamente o caminho absoluto e os parâmetros esperados
    args, kwargs = mock_run.call_args
    assert args[0] == [
        "/usr/bin/podman-compose",
        "-f",
        str(Path.cwd() / lab_id / "docker-compose.yml"),
        "up",
        "-d",
    ]
    assert kwargs["check"] is True


def test_run_handles_podman_error():
    # Arrange
    adapter = PodmanComposeLabLifecycle()
    mock_run = MagicMock()

    # Simula o erro
    mock_run.side_effect = subprocess.CalledProcessError(
        returncode=1, cmd="/usr/bin/podman-compose", output="", stderr="Error: container not found"
    )

    # Força o mock no método que você quer testar
    with patch("subprocess.run", mock_run):
        try:
            adapter.run("teste-pr019")
        except Exception as e:
            # Assert: verifica se é o tipo correto e a mensagem
            assert type(e).__name__ == "LabExecutionError"
            assert "Erro no Podman: Error: container not found" in str(e)
            return  # Teste passou!

    # Se chegar aqui, nenhuma exceção foi levantada
    pytest.fail("LabExecutionError não foi levantado pelo adaptador!")


@patch("subprocess.run")
def test_status_returns_running_state(mock_run):
    # Arrange
    adapter = PodmanComposeLabLifecycle()
    mock_run.return_value = MagicMock(stdout="Up 2 minutes")

    # Act
    status = adapter.status("teste-pr019")

    # Assert
    from cyberlab.domain.models.lab_execution_report import LaboratoryState

    assert status.state == LaboratoryState.RUNNING


def test_deploy_starts_the_lab_from_the_manifest_path() -> None:
    adapter = PodmanComposeLabLifecycle()

    with patch.object(adapter, "run", return_value=MagicMock(message="started")) as run:
        result = adapter.deploy("/workspace/labs/demo/lab.yaml")

    assert result == "started"
    run.assert_called_once_with("demo")


@patch("subprocess.run")
def test_exec_uses_podman_container(mock_run) -> None:
    adapter = PodmanComposeLabLifecycle()
    mock_run.side_effect = [
        MagicMock(stdout="demo-web-1\n"),
        MagicMock(returncode=0, stdout="uid=0\n", stderr=""),
    ]

    result = adapter.exec("demo", "id")

    assert result == "uid=0"
    assert mock_run.call_args_list[1].args[0] == ["podman", "exec", "demo-web-1", "sh", "-c", "id"]


@patch("subprocess.run")
def test_proxy_reports_published_podman_ports(mock_run) -> None:
    adapter = PodmanComposeLabLifecycle()
    mock_run.side_effect = [
        MagicMock(stdout="demo-web-1\n"),
        MagicMock(returncode=0, stdout="80/tcp -> 127.0.0.1:8080\n", stderr=""),
    ]

    result = adapter.proxy("demo")

    assert result == "Endpoint(s) publicado(s) para 'demo':\n80/tcp -> 127.0.0.1:8080"
    assert mock_run.call_args_list[1].args[0] == ["podman", "port", "demo-web-1"]
