from cyberlab.application.interfaces.lab_repository_protocol import (
    LabRepositoryProtocol,
)
from cyberlab.domain.models.lab import Lab


class ListLabsUseCase:
    """List available CyberLab laboratories."""

    def __init__(
        self,
        repository: LabRepositoryProtocol,
    ) -> None:
        self._repository = repository

    def execute(self) -> tuple[Lab, ...]:
        """Return all available laboratories."""
        return self._repository.list()
