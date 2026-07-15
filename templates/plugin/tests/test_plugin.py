from cyberlab_plugin_hello.plugin import HelloPlugin

from cyberlab.sdk import PluginProtocol


def test_plugin_manifest() -> None:
    plugin = HelloPlugin()

    assert plugin.manifest.id == "hello-plugin"
    assert plugin.manifest.name == "Hello Plugin"
    assert isinstance(plugin, PluginProtocol)
