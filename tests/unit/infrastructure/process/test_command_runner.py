from cyberlab.infrastructure.process.command_runner import CommandRunner


def test_run_python_version() -> None:
    runner = CommandRunner()

    result = runner.run(["python", "--version"])

    assert result.exit_code == 0
    assert "Python" in result.stdout


def test_run_unknown_command() -> None:
    runner = CommandRunner()

    result = runner.run(["command-that-does-not-exist"])

    assert result.exit_code != 0
