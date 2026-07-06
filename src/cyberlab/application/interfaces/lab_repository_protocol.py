from typing import Protocol

from cyberlab.domain.models.lab import Lab


class LabRepositoryProtocol(Protocol):
    """Provides access to CyberLab laboratories."""

    def list(self) -> tuple[Lab, ...]:
        """Return all available laboratories."""
        ...
