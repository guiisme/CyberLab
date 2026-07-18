import yaml

from cyberlab.infrastructure.environment import CYBERLAB_HOME
from cyberlab_plugin_k8s.infrastructure.k8s_lifecycle import KubernetesLifecycle
from cyberlab_plugin_podman.infrastructure.podman_compose import PodmanComposeLabLifecycle


# Correção: Adicionado o argumento lab_id
def get_lifecycle_adapter(lab_id: str):
    # Correção: Uso da constante CYBERLAB_HOME para consistência
    lab_path = CYBERLAB_HOME / "labs" / lab_id
    config_file = lab_path / "lab.yaml"

    if not config_file.exists():
        raise Exception(f"Arquivo de configuração 'lab.yaml' não encontrado em {lab_path}")

    with open(config_file) as f:
        docs = list(yaml.safe_load_all(f))

    if not docs:
        raise Exception("O arquivo lab.yaml está vazio.")

    lab_config = docs[0] if isinstance(docs[0], dict) else {}
    engine = lab_config.get("engine", "k8s").lower()

    if engine == "k8s":
        return KubernetesLifecycle(lab_id=lab_id)
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
        expected_flag = config.get("flag")

    return submitted_flag == expected_flag
