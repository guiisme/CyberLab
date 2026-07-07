from __future__ import annotations

from typing import Protocol

from cyberlab.domain.models.lab_manifest import LabManifest


class LabManifestLoaderProtocol(Protocol):
    """Load a laboratory manifest."""

    def load(
        self,
        lab_id: str,
    ) -> LabManifest:
        """Load the manifest for a laboratory."""
        ...
