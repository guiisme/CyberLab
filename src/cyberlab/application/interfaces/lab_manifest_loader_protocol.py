from typing import Protocol

from cyberlab.domain.models.lab_manifest import LabManifest


class LabManifestLoaderProtocol(Protocol):
    """Load laboratory metadata."""

    def load(
        self,
        lab_id: str,
    ) -> LabManifest:
        """Load a laboratory manifest."""
        ...
