from __future__ import annotations

from cyberlab.application.interfaces.lab_scaffolding_protocol import (
    LabScaffoldingProtocol,
)


class FakeLabScaffolding(LabScaffoldingProtocol):
    """Fake laboratory scaffolding."""

    def __init__(self) -> None:
        self.created_labs: list[tuple[str, str, str]] = []

    def create(
        self,
        lab_id: str,
        scaffold: str = "default",
        profile: str = "web",
    ) -> None:
        self.created_labs.append(
            (
                lab_id,
                scaffold,
                profile,
            ),
        )
