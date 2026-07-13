from __future__ import annotations

from typing import Protocol


class LabScaffoldingProtocol(Protocol):
    """Protocol for laboratory scaffolding."""

    def create(
        self,
        lab_id: str,
        scaffold: str = "default",
    ) -> None:
        """Create a new laboratory from a scaffold."""
