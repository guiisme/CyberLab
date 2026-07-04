from __future__ import annotations

import re

from cyberlab.shared.version import get_version

SEMVER_PATTERN = r"^\d+\.\d+\.\d+$"


def test_get_version_returns_string() -> None:
    """The version must be returned as a string."""
    version = get_version()

    assert isinstance(version, str)


def test_get_version_is_not_empty() -> None:
    """The version string must not be empty."""
    version = get_version()

    assert version


def test_get_version_matches_semver() -> None:
    """The version must follow semantic versioning."""
    version = get_version()

    assert re.fullmatch(SEMVER_PATTERN, version)
