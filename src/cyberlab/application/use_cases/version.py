from __future__ import annotations

from cyberlab.shared.version import get_version as shared_get_version


def get_version() -> str:
    """Return the current CyberLab version."""

    return shared_get_version()
