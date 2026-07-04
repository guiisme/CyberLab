from __future__ import annotations

from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as package_version

PACKAGE_NAME = "cyberlab"


def get_version() -> str:
    """Return the installed CyberLab version."""

    try:
        return package_version("cyberlab")
    except PackageNotFoundError:
        return "0.0.0-dev"
