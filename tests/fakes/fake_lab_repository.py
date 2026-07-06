from cyberlab.application.interfaces.lab_repository_protocol import (
    LabRepositoryProtocol,
)
from cyberlab.domain.models.lab import Lab


class FakeLabRepository(LabRepositoryProtocol):
    """In-memory implementation of LabRepositoryProtocol."""

    def __init__(
        self,
        labs: tuple[Lab, ...] = (),
    ) -> None:
        self._labs = labs

    def list(self) -> tuple[Lab, ...]:
        return self._labs
