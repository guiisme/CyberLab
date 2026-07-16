from pathlib import Path

import yaml

from cyberlab_plugin_k8s.infrastructure.k8s_lifecycle import KubernetesLifecycle

# Importe os seus adaptadores aqui
from cyberlab_plugin_podman.infrastructure.podman_compose import PodmanComposeLabLifecycle


def get_lifecycle_adapter(lab_id: str):
    lab_path = Path.cwd() / "labs" / lab_id / "lab.yaml"

    if not lab_path.exists():
        raise FileNotFoundError(f"Lab {lab_id} não possui um lab.yaml definido.")

    with open(lab_path) as f:
        config = yaml.safe_load(f)

    engine = config.get("engine", "podman").lower()

    if engine == "k8s":
        return KubernetesLifecycle()
    elif engine == "podman":
        return PodmanComposeLabLifecycle()
    else:
        raise ValueError(f"Engine '{engine}' não suportada para o lab {lab_id}.")
