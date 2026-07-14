from src.cyberlab_plugin_hello.plugin import HelloPlugin


def test_plugin_manifest() -> None:
    plugin = HelloPlugin()

    assert plugin.manifest.id == "hello-plugin"
    from cyberlab.sdk import PluginProtocol

    assert isinstance(plugin, PluginProtocol)
