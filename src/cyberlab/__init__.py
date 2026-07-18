"""CyberLab package."""

from __future__ import annotations

from typing import Any

__all__ = ["get_lifecycle_adapter"]


def __getattr__(name: str) -> Any:
    """Lazily expose runtime wiring without import-time cycles."""

    if name == "get_lifecycle_adapter":
        from cyberlab.registry import get_lifecycle_adapter

        return get_lifecycle_adapter
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
