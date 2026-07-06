from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LabManifest:
    """Metadata describing a CyberLab laboratory."""

    id: str
    name: str
    description: str
    category: str
    difficulty: str
    version: str
