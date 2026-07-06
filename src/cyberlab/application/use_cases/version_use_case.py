from __future__ import annotations

from cyberlab.shared.version import get_version as shared_get_version


class VersionUseCase:
    """Return the current CyberLab version."""

    def execute(self) -> str:
        """Return the current CyberLab version."""

        return shared_get_version()
