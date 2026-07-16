from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LabLogs:
    """Laboratory logs."""

    content: str
    lab_id: str
