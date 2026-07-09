from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LabExecutionResult:
    """Represents the result of a laboratory execution."""

    success: bool
    message: str
