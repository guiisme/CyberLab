from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from cyberlab.application.interfaces.lab_manifest_loader_protocol import (
    LabManifestLoaderProtocol,
)
from cyberlab.domain.models.lab_manifest import LabManifest


class YamlLabManifestLoader(LabManifestLoaderProtocol):
    """Load laboratory metadata from a YAML manifest."""

    def __init__(self, labs_root: Path) -> None:
        self._labs_root = labs_root

    def load(self, lab_id: str) -> LabManifest:
        """Load a laboratory manifest."""

        manifest_path = self._labs_root.joinpath(
            lab_id,
            "lab.yaml",
        )

        with manifest_path.open(encoding="utf-8") as file:
            data: dict[str, Any] = yaml.safe_load(file)

        return LabManifest(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            category=data["category"],
            difficulty=data["difficulty"],
            version=data["version"],
        )
