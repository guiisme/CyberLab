"""Compatibility facade for the pre-Typer command-line interface."""

from cyberlab.infrastructure.environment import (
    create_lab_template,
    pre_flight_check,
    setup_workspace,
)
from cyberlab.registry import get_lifecycle_adapter, validate_flag

__all__ = [
    "create_lab_template",
    "get_lifecycle_adapter",
    "pre_flight_check",
    "setup_workspace",
    "validate_flag",
]
