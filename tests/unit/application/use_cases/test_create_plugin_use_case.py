class FakePluginScaffolding:
    def __init__(self) -> None:
        self.received_plugin_id: str | None = None

    def create(self, plugin_id: str) -> None:
        self.received_plugin_id = plugin_id


"""     def test_execute_creates_plugin() -> None:
    scaffolding = FakePluginScaffolding()

    use_case = CreatePluginUseCase(scaffolding)

    use_case.execute("hello")

    assert scaffolding.received_plugin_id == "hello" """
