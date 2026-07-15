from cyberlab_plugin_hello.plugin import Podman

from cyberlab.sdk import PluginProtocol


def test_plugin_manifest() -> None:
    plugin = Podman()

    assert plugin.manifest.id == "podman"
    assert plugin.manifest.name == "Podman"
    assert isinstance(plugin, PluginProtocol)
