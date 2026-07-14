from cyberlab.sdk import (
    Plugin,
    PluginManifest,
    PluginProtocol,
)


def test_sdk_exports() -> None:
    assert Plugin is not None
    assert PluginManifest is not None
    assert PluginProtocol is not None
