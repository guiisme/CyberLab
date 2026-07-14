import pytest

from cyberlab.infrastructure.plugins.plugin_registry import PluginRegistry
from tests.fakes.fake_plugin import FakePlugin


def test_registry_starts_empty() -> None:
    registry = PluginRegistry()

    assert registry.all() == ()


def test_register_plugin() -> None:
    registry = PluginRegistry()
    plugin = FakePlugin()

    registry.register(plugin)

    assert registry.has(plugin.manifest.id)


def test_get_registered_plugin() -> None:
    registry = PluginRegistry()
    plugin = FakePlugin()

    registry.register(plugin)

    assert registry.get(plugin.manifest.id) is plugin


def test_get_unknown_plugin_returns_none() -> None:
    registry = PluginRegistry()

    assert registry.get("unknown") is None


def test_has_returns_false_for_unknown_plugin() -> None:
    registry = PluginRegistry()

    assert not registry.has("unknown")


def test_register_duplicate_plugin_raises_error() -> None:
    registry = PluginRegistry()

    plugin = FakePlugin()

    registry.register(plugin)

    with pytest.raises(ValueError):
        registry.register(plugin)


def test_all_returns_registered_plugins() -> None:
    registry = PluginRegistry()

    plugin1 = FakePlugin("plugin-1")
    plugin2 = FakePlugin("plugin-2")

    registry.register(plugin1)
    registry.register(plugin2)

    plugins = registry.all()

    assert plugins == (plugin1, plugin2)


def test_all_returns_tuple() -> None:
    registry = PluginRegistry()

    assert isinstance(registry.all(), tuple)
