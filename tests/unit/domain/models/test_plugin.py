import pytest

from cyberlab.domain.models.plugin import Plugin
from cyberlab.domain.models.plugin_manifest import PluginManifest


def test_plugin_store_manifest() -> None:
    manifest = PluginManifest(
        id="example-plugin",
        name="Example Plugin",
        version="1.0.0",
        description="An example plugin for CyberLab.",
        author="John Doe",
        capabilities=("capability1", "capability2"),
    )
    plugin = Plugin(manifest=manifest)

    assert plugin.manifest == manifest


def test_plugin_is_immutable() -> None:
    plugin = Plugin(
        manifest=PluginManifest(
            id="example-plugin",
            name="Example Plugin",
            version="1.0.0",
            description="An example plugin for CyberLab.",
            author="John Doe",
            capabilities=("capability1", "capability2"),
        )
    )

    with pytest.raises(AttributeError):
        plugin.manifest = plugin.manifest  # type: ignore[misc]


def test_plugin_instances_with_same_manifest_are_equal() -> None:
    manifest = PluginManifest(
        id="example-plugin",
        name="Example Plugin",
        version="1.0.0",
        description="An example plugin for CyberLab.",
        author="John Doe",
        capabilities=("capability1", "capability2"),
    )
    first_plugin = Plugin(manifest=manifest)
    second_plugin = Plugin(manifest=manifest)

    assert first_plugin == second_plugin
