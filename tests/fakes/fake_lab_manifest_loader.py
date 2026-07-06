from __future__ import annotations

from cyberlab.application.interfaces.lab_manifest_loader_protocol import (
    LabManifestLoaderProtocol,
)
from cyberlab.domain.models.lab_manifest import LabManifest


class FakeLabManifestLoader(LabManifestLoaderProtocol):
    """In-memory implementation of LabManifestLoaderProtocol."""

    def __init__(
        self,
        manifests: dict[str, LabManifest],
    ) -> None:
        self._manifests = manifests
        self.requested_lab_ids: list[str] = []

    def load(
        self,
        lab_id: str,
    ) -> LabManifest:
        """Load a laboratory manifest."""

        self.requested_lab_ids.append(lab_id)

        if lab_id not in self._manifests:
            raise AssertionError(f"Unexpected lab id: {lab_id}")

        return self._manifests[lab_id]
