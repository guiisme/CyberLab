import subprocess
import time


def start_port_forward(
    lab_id: str, local_port: int = 8080, remote_port: int = 80
) -> subprocess.Popen:
    cmd = ["kubectl", "port-forward", f"deployment/{lab_id}", f"{local_port}:{remote_port}"]

    # Garantimos stderr=subprocess.PIPE para que nunca seja None
    process = subprocess.Popen(cmd, stderr=subprocess.PIPE, text=True)

    time.sleep(2)

    if process.poll() is not None:
        # Agora o Pylance entende que, se entramos aqui, o stderr não será None
        stderr_output = process.stderr.read() if process.stderr else "Erro desconhecido"
        raise RuntimeError(f"Falha ao iniciar port-forward: {stderr_output}")

    return process
