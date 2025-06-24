import builtins
import pytest

import shell

from src.shell_commands.shell_command import ShellCommand


def simulate_shell(inputs, monkeypatch):
    input_iter = iter(inputs)

    def mock_input(_):
        return next(input_iter)

    monkeypatch.setattr(builtins, "input", mock_input)


def test_eixt_정상명령(monkeypatch, capsys):
    simulate_shell(["exit"], monkeypatch)

    shell.shell_mode()

    captured = capsys.readouterr()

    assert "[EXIT]" in captured.out


def test_eixt_많은인자(monkeypatch, capsys):
    simulate_shell(["exit 0", "exit"], monkeypatch)

    shell.shell_mode()

    captured = capsys.readouterr()

    assert "takes no arguments, but got" in captured.out
    assert "[EXIT]" in captured.out
