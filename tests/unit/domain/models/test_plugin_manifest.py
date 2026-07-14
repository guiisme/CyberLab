from dataclasses import FrozenInstanceError

import pytest

from cyberlab.domain.models.plugin_manifest import PluginManifest


def test_create_plugin_manifest() -> None:
    manifest = PluginManifest(
        id="example-plugin",
        name="Example Plugin",
        version="1.0.0",
        description="An example plugin for CyberLab.",
        author="John Doe",
        capabilities=("capability1", "capability2"),
    )

    assert manifest.id == "example-plugin"
    assert manifest.name == "Example Plugin"
    assert manifest.version == "1.0.0"
    assert manifest.description == "An example plugin for CyberLab."
    assert manifest.author == "John Doe"
    assert manifest.capabilities == ("capability1", "capability2")


def test_plugin_manifest_is_immutable() -> None:
    # Arrange
    manifest = PluginManifest(
        id="example-plugin",
        name="Example Plugin",
        version="1.0.0",
        description="An example plugin for CyberLab.",
        author="John Doe",
        capabilities=("capability1", "capability2"),
    )

    # Act / Assert
    with pytest.raises(FrozenInstanceError):
        manifest.name = "New Name"


def test_plugin_manifests_with_same_values_are_equal() -> None:
    first = PluginManifest(
        id="example-plugin",
        name="Example Plugin",
        version="1.0.0",
        description="An example plugin for CyberLab.",
        author="John Doe",
        capabilities=("capability1", "capability2"),
    )

    second = PluginManifest(
        id="example-plugin",
        name="Example Plugin",
        version="1.0.0",
        description="An example plugin for CyberLab.",
        author="John Doe",
        capabilities=("capability1", "capability2"),
    )

    assert first == second


def test_plugin_manifests_with_different_values_are_not_equal() -> None:
    first = PluginManifest(
        id="example-plugin",
        name="Example Plugin",
        version="1.0.0",
        description="An example plugin for CyberLab.",
        author="John Doe",
        capabilities=("capability1", "capability2"),
    )

    second = PluginManifest(
        id="different-plugin",
        name="Different Plugin",
        version="2.0.0",
        description="A different plugin for CyberLab.",
        author="Jane Smith",
        capabilities=("capability3",),
    )

    assert first != second


def test_plugin_manifest_with_empty_capabilities() -> None:
    manifest = PluginManifest(
        id="example-plugin",
        name="Example Plugin",
        version="1.0.0",
        description="An example plugin for CyberLab.",
        author="John Doe",
        capabilities=(),
    )

    assert manifest.capabilities == ()


def test_plugin_manifest_with_multiple_capabilities() -> None:
    manifest = PluginManifest(
        id="example-plugin",
        name="Example Plugin",
        version="1.0.0",
        description="An example plugin for CyberLab.",
        author="John Doe",
        capabilities=("capability1", "capability2", "capability3"),
    )

    assert manifest.capabilities == ("capability1", "capability2", "capability3")
