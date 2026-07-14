from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol

from cyberlab.application.interfaces.plugin_protocol import PluginProtocol


class PluginLoaderProtocol(Protocol):
    def load(self) -> Sequence[PluginProtocol]: ...
