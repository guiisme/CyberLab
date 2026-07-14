from collections.abc import Sequence

from tests.fakes.fake_entry_point import FakeEntryPoint


class FakeEntryPointProvider:
    """Fake provider used by PluginLoader tests."""

    def __init__(
        self,
        entry_points: Sequence[FakeEntryPoint],
    ) -> None:
        self._entry_points = tuple(entry_points)

    def entry_points(self) -> Sequence[FakeEntryPoint]:
        return self._entry_points
