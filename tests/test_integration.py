import builtins
import pytest

from src import shell

from src.commands.command_action import CommandAction
from src.ssd_driver import SSDDriver


def simulate_shell(inputs, monkeypatch):
    input_iter = iter(inputs)

    def mock_input(_):
        return next(input_iter)

    monkeypatch.setattr(builtins, "input", mock_input)


@pytest.mark.parametrize('operation, expected',
                         [
                             ('write 0 0x12345678', "[WRITE] Done"),
                             ('read 0', "[READ] LBA 0 : 0x12345678"),
                             ('fullwrite 0x87654321', ""),
                             ('fullread', "[FULLREAD] 0 0x87654321"),
                             ('1_FullWriteAndReadCompare', "[1_FULLWRITEANDREADCOMPARE] PASS"),
                             ('1_', "[1_FULLWRITEANDREADCOMPARE] PASS"),
                             ('2_PartialLBAWrite', "[2_PARTIALLBAWRITE] PASS"),
                             ('2_', "[2_PARTIALLBAWRITE] PASS"),
                             ('3_WriteReadAging', "[3_WRITEREADAGING] PASS"),
                             ('3_', "[3_WRITEREADAGING] PASS"),
                         ])
def test_통합테스트_정상명령어(monkeypatch, capsys, operation, expected):
    simulate_shell([operation, 'exit'], monkeypatch)

    shell.shell_mode(SSDDriver())

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

    shell.shell_mode(SSDDriver())

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

    shell.shell_mode(SSDDriver())

    captured = capsys.readouterr()

    assert expected in captured.out
    assert "[EXIT]" in captured.out
