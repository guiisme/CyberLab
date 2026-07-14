from collections.abc import Sequence
from importlib.metadata import EntryPoint, entry_points


class EntryPointProvider:
    """Provides CyberLab plugin entry points."""

    GROUP = "cyberlab.plugins"

    def entry_points(self) -> Sequence[EntryPoint]:
        return entry_points(group=self.GROUP)
