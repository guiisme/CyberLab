from typing import Any


class FakeEntryPoint:
    """Simple fake implementation of a Python EntryPoint."""

    def __init__(self, plugin_class: type[Any]) -> None:
        self._plugin_class = plugin_class

    def load(self) -> type[Any]:
        return self._plugin_class
