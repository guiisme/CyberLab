"""
Technical utilities for retrieving CyberLab package version.

This module belongs to the shared package because it provides
application-wide technical metadata and does not belong to any
architectural layer.
"""

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
