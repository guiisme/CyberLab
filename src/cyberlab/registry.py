from pathlib import Path

import yaml

from cyberlab.infrastructure.environment import CYBERLAB_HOME
from cyberlab_plugin_k8s.infrastructure.k8s_lifecycle import KubernetesLifecycle
from cyberlab_plugin_podman.infrastructure.podman_compose import PodmanComposeLabLifecycle


def get_lifecycle_adapter(lab_id: str):
    lab_path = Path.home() / "CyberLab/labs" / lab_id
    config_file = lab_path / "lab.yaml"

    if not config_file.exists():
        raise Exception(f"Arquivo de configuração 'lab.yaml' não encontrado em {lab_path}")

    with open(config_file) as f:
        # Usamos safe_load_all para processar todos os documentos,
        # mas pegamos apenas o primeiro para verificar a 'engine'
        docs = list(yaml.safe_load_all(f))

    if not docs:
        raise Exception("O arquivo lab.yaml está vazio.")

    # Tentamos pegar a engine do primeiro documento (ou de um documento de config dedicado)
    # Se o primeiro documento for um Namespace, o .get não vai falhar, retornará None
    # Então definimos um padrão seguro:
    lab_config = docs[0] if isinstance(docs[0], dict) else {}
    engine = lab_config.get(
        "engine", "k8s"
    ).lower()  # Defini como 'k8s' por padrão já que você está usando K8s

    if engine == "k8s":
        return KubernetesLifecycle()
    elif engine == "podman":
        return PodmanComposeLabLifecycle()
    else:
        raise ValueError(f"Engine '{engine}' não suportada para o lab {lab_id}.")


def validate_flag(lab_id: str, submitted_flag: str) -> bool:
    lab_yaml_path = CYBERLAB_HOME / "labs" / lab_id / "lab.yaml"

    if not lab_yaml_path.exists():
        return False

    with open(lab_yaml_path) as f:
        config = yaml.safe_load(f)
        # Supondo que a flag esteja salva no campo 'flag' do lab.yaml
        expected_flag = config.get("flag")

    return submitted_flag == expected_flag
