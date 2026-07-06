from dataclasses import dataclass

from cyberlab.domain.models.lab import Lab


@dataclass(frozen=True, slots=True)
class LabListReport:
    """Result of listing available laboratories."""

    labs: tuple[Lab, ...]
