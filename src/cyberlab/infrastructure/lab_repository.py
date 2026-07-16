from pathlib import Path
from typing import Any

import yaml


class LabRepository:
    def __init__(self, labs_root: Path):
        self.labs_root = labs_root

    def get_all_labs(self) -> list[dict[str, Any]]:
        labs = []
        if not self.labs_root.exists():
            return labs

        for lab_dir in self.labs_root.iterdir():
            lab_yaml = lab_dir / "lab.yaml"
            if lab_yaml.exists():
                with open(lab_yaml) as f:
                    data = yaml.safe_load(f)
                    # Adiciona metadados úteis para a CLI
                    data["engine"] = "K8s" if (lab_dir / "k8s").exists() else "Podman"
                    labs.append(data)
        return labs
