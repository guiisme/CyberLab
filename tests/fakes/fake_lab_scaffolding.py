from __future__ import annotations

from cyberlab.application.interfaces.lab_scaffolding_protocol import (
    LabScaffoldingProtocol,
)


class FakeLabScaffolding(LabScaffoldingProtocol):
    """Fake laboratory scaffolding."""

    def __init__(self) -> None:
        self.created = []

    def create(
        self,
        lab_id: str,
        scaffold: str = "default",
    ) -> None:
        self.created.append(
            (
                lab_id,
                scaffold,
            ),
        )
