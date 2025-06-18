import builtins
import pytest

from src import shell
from src.command_action import CommandAction


@pytest.fixture
def mock_handler_and_driver(mocker):
    mock_driver = mocker.Mock()
    mock_handler = mocker.Mock()
    mock_handler_instance = mocker.Mock()
    mock_handler.return_value = mock_handler_instance
    mocker.patch("src.ssd.VirtualSSD", return_value=mock_driver)

    return mock_driver, mock_handler, mock_handler_instance


def simulate_shell(inputs, monkeypatch):
    input_iter = iter(inputs)

    def mock_input(_):
        return next(input_iter)

    monkeypatch.setattr(builtins, "input", mock_input)


def test_shell_일반적인_명령어(monkeypatch, capsys, mock_handler_and_driver):
    mock_driver, mock_handler, mock_handler_instance = mock_handler_and_driver
    mock_handler_instance.run.return_value = "Done"

    CommandAction.registry["write"] = mock_handler

    simulate_shell(["write arg1 arg2", "exit"], monkeypatch)

    shell.main()

    captured = capsys.readouterr()
    assert "[WRITE] Done" in captured.out
    assert "[EXIT]" in captured.out


def test_shell_help_명령어_목록_출력(monkeypatch, capsys, mocker):
    class DummyCommand(CommandAction):
        command_name = ['read']
        description = 'Read from SSD'
        usage = 'read <LBA>'
        author = 'Tester'
        alias = ['r']

        def run(self): pass

        def validate(self): return True

    class HelpCommand(CommandAction):
        command_name = ['help']
        description = 'Show help'
        usage = 'help'
        author = 'Tester'
        alias = ['h']

        def run(self):
            if not self.validate():
                raise Exception()
            for name in CommandAction.registry:
                print(f"▶ {name}")

        def validate(self):
            return len(self._arguments) == 0

    CommandAction.registry.clear()
    CommandAction.registry['help'] = HelpCommand
    CommandAction.registry['read'] = DummyCommand

    mocker.patch("src.ssd.VirtualSSD", return_value=mocker.Mock())
    simulate_shell(["help", "exit"], monkeypatch)

    shell.main()
    captured = capsys.readouterr()

    assert "▶ help" in captured.out
    assert "▶ read" in captured.out
    assert "[EXIT]" in captured.out


def test_shell_없는_명령어_입력_시_invalid_command_확인(monkeypatch, capsys, mocker):
    mocker.patch("src.ssd.VirtualSSD", return_value=mocker.Mock())
    simulate_shell(["foobar", "exit"], monkeypatch)

    shell.main()

    captured = capsys.readouterr()
    assert "[FOOBAR] INVALID COMMAND" in captured.out
    assert "[EXIT]" in captured.out


def test_shell_exception_뜨면_안멈추고_메시지_띄우는지(monkeypatch, capsys, mock_handler_and_driver):
    mock_driver, mock_handler, mock_handler_instance = mock_handler_and_driver

    def broken_run(*args):
        raise Exception("boom")

    mock_handler_instance.run.side_effect = broken_run

    CommandAction.registry["explode"] = mock_handler

    simulate_shell(["explode", "exit"], monkeypatch)

    shell.main()

    captured = capsys.readouterr()
    assert "[ERROR] boom" in captured.out
    assert "[EXIT]" in captured.out
