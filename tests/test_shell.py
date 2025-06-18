import builtins
import pytest

from src import shell

from src.commands.command_action import CommandAction
from src.ssd_driver import SSDDriver


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


def test_shell_없는_명령어_입력_시_invalid_command_확인(monkeypatch, capsys, mocker):
    mocker.patch("src.ssd.VirtualSSD", return_value=mocker.Mock())
    simulate_shell(["foobar", "exit"], monkeypatch)

    shell.main()

    captured = capsys.readouterr()
    assert "[FOOBAR] INVALID COMMAND" in captured.out
    assert "[EXIT]" in captured.out


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
        command_name = 'dummy'
        description = 'Test Dummy'
        usage = 'dummy <LBA>'
        author = 'Tester'
        alias = ['du']

        def run(self): pass

        def validate(self): return True

    mocker.patch("src.ssd.VirtualSSD", return_value=mocker.Mock())
    simulate_shell(["help", "exit"], monkeypatch)

    shell.main()
    captured = capsys.readouterr()

    assert "▶ help" in captured.out
    assert "▶ dummy" in captured.out
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


@pytest.mark.parametrize('operation, expected',
                         [
                             ('write 0 0x12345678', "[WRITE] Done"),
                             ('read 1', "[READ] LBA 00 : 0x00000000"),
                             ('fullwrite 0x87654321', ""),
                             ('fullread', "[FULLREAD] 0 0x87654321"),
                             ('1_FullWriteAndReadCompare', "[1_FULLWRITEANDREADCOMPARE] PASS"),
                             ('2_PartialLBAWrite', "[2_PARTIALLBAWRITE] PASS"),
                             ('3_WriteReadAging', "[3_WRITEREADAGING] PASS"),
                         ])
def test_통합테스트_정상명령어(monkeypatch, capsys, operation, expected):
    simulate_shell([operation, 'exit'], monkeypatch)

    shell.main(SSDDriver())

    captured = capsys.readouterr()

    assert expected in captured.out
    assert "[EXIT]" in captured.out


@pytest.mark.parametrize('operation, expected',
                         [
                             ('write 0', "[ERROR]"),
                             ('write 0 0x12345678 1', "[ERROR]"),
                             ('read', "[ERROR]"),
                             ('read 0 0x12345678', "[ERROR]"),
                             ('fullwrite', "[ERROR]"),
                             ('fullwrite 0 0x12345678', "[ERROR]"),
                             ('fullread 0', "[ERROR]")
                         ])
def test_통합테스트_argument_개수틀림(monkeypatch, capsys, operation, expected):
    simulate_shell([operation, 'exit'], monkeypatch)

    shell.main(SSDDriver())

    captured = capsys.readouterr()

    assert expected in captured.out
    assert "[EXIT]" in captured.out


@pytest.mark.parametrize('operation, expected',
                         [
                             ('write 0 0x1234567', "[ERROR]"),
                             ('write c 0x1234567', "[ERROR]"),
                             ('read a', "[ERROR]"),
                             ('fullwrite 0x1234567', "[ERROR]"),
                         ])
def test_통합테스트_argument_형식틀림(monkeypatch, capsys, operation, expected):
    simulate_shell([operation, 'exit'], monkeypatch)

    shell.main(SSDDriver())

    captured = capsys.readouterr()

    assert expected in captured.out
    assert "[EXIT]" in captured.out
