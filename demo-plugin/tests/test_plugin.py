from cyberlab_plugin_hello.plugin import DemoPlugin

from cyberlab.sdk import PluginProtocol


def test_plugin_manifest() -> None:
    plugin = DemoPlugin()

    assert plugin.manifest.id == "demo-plugin"
    assert plugin.manifest.name == "Demo Plugin"
    assert isinstance(plugin, PluginProtocol)
