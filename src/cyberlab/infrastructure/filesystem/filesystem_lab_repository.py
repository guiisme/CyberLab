from pathlib import Path

from cyberlab.application.interfaces.lab_repository_protocol import (
    LabRepositoryProtocol,
)
from cyberlab.domain.models.lab import Lab


class FilesystemLabRepository(LabRepositoryProtocol):
    """Repository that discovers laboratories from the filesystem."""

    def __init__(self, labs_root: Path) -> None:
        self._labs_root = labs_root

    def list(self) -> tuple[Lab, ...]:
        directories = (path for path in self._labs_root.iterdir() if path.is_dir())

        labs = sorted(
            (Lab(path.name) for path in directories),
            key=lambda lab: lab.name,
        )

        return tuple(labs)
