from __future__ import annotations

from cyberlab.application.interfaces.lab_manifest_loader_protocol import (
    LabManifestLoaderProtocol,
)
from cyberlab.domain.models.lab_manifest import LabManifest


class LabInfoUseCase:
    """Return metadata for a laboratory."""

    def __init__(
        self,
        loader: LabManifestLoaderProtocol,
    ) -> None:
        self._loader = loader

    def execute(
        self,
        lab_id: str,
    ) -> LabManifest:
        """Return the laboratory metadata."""

        return self._loader.load(lab_id)
