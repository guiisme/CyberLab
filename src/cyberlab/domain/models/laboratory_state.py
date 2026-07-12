from enum import StrEnum


class LaboratoryState(StrEnum):
    """Represents the execution state of a laboratory."""

    RUNNING = "running"
    STOPPED = "stopped"
