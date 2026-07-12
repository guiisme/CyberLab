from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LabLogs:
    """Laboratory logs."""

    lab_id: str
    content: str
