from __future__ import annotations

from cyberlab.application.interfaces.lab_scaffolding_protocol import (
    LabScaffoldingProtocol,
)


class LabCreateUseCase:
    """Use case for creating laboratories from scaffolds."""

    def __init__(
        self,
        scaffolding: LabScaffoldingProtocol,
    ) -> None:
        self._scaffolding = scaffolding

    def execute(
        self,
        lab_id: str,
        scaffold: str = "default",
        profile: str = "web",
    ) -> None:
        """Create a laboratory."""

        self._scaffolding.create(
            lab_id=lab_id,
            scaffold=scaffold,
            profile=profile,
        )
