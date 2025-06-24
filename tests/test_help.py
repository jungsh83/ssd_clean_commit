import builtins
import pytest
import shell
from src.shell_commands.shell_command import ShellCommand

FILEMANAGER_SOURCE_PATH = "src.ssd_file_manager.SSDFileManager"


def simulate_shell(inputs, monkeypatch):
    input_iter = iter(inputs)

    def mock_input(_):
        return next(input_iter)

    monkeypatch.setattr(builtins, "input", mock_input)


def test_help_정상명령(monkeypatch, capsys, mocker):
    class DummyShellCommand(ShellCommand):
        command_name = 'dummy'
        description = 'Test Dummy'
        usage = 'dummy <LBA>'
        author = 'Tester'
        alias = ['du']

        def execute(self): pass

        def validate(self): return True

    mocker.patch(FILEMANAGER_SOURCE_PATH, return_value=mocker.Mock())
    simulate_shell(["help", "exit"], monkeypatch)

    shell.shell_mode()
    captured = capsys.readouterr()

    assert "▶ help" in captured.out
    assert "▶ dummy" in captured.out
    assert "[EXIT]" in captured.out


def test_help_많은인자(monkeypatch, capsys, mocker):
    class DummyShellCommand(ShellCommand):
        command_name = 'dummy'
        description = 'Test Dummy'
        usage = 'dummy <LBA>'
        author = 'Tester'
        alias = ['du']

        def execute(self): pass

        def validate(self): return True

    mocker.patch(FILEMANAGER_SOURCE_PATH, return_value=mocker.Mock())
    simulate_shell(["help 0", "exit"], monkeypatch)

    shell.shell_mode()
    captured = capsys.readouterr()

    assert "takes no arguments, but got" in captured.out
    assert "[EXIT]" in captured.out
