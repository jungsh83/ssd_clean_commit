import builtins
import pytest

from ssd_clean_commit.src import shell
from ssd_clean_commit.src.command_action import CommandAction


@pytest.fixture
def mock_registry_and_driver(mocker):
    mock_driver = mocker.Mock()
    mock_handler = mocker.Mock()
    mock_handler_instance = mocker.Mock()
    mock_handler.return_value = mock_handler_instance
    mock_handler_instance.run_test.return_value = "PASS"

    CommandAction.registry["read"] = mock_handler

    mocker.patch("ssd_clean_commit.src.shell.DummySSDDriver", return_value=mock_driver)
    return mock_driver, mock_handler, mock_handler_instance


def simulate_shell(inputs, monkeypatch):
    input_iter = iter(inputs)

    def mock_input(_):
        return next(input_iter)

    monkeypatch.setattr(builtins, "input", mock_input)


def test_shell_일반적인_명령어(monkeypatch, capsys, mock_registry_and_driver):
    simulate_shell(["read arg1 arg2", "exit"], monkeypatch)

    shell.main()

    captured = capsys.readouterr()
    assert "[READ] PASS" in captured.out
    assert "[EXIT]" in captured.out


def test_shell_없는_명령어_입력_시_invalid_command_확인(monkeypatch, capsys, mocker):
    mocker.patch("ssd_clean_commit.src.shell.DummySSDDriver", return_value=mocker.Mock())
    simulate_shell(["foobar", "exit"], monkeypatch)

    shell.main()

    captured = capsys.readouterr()
    assert "[FOOBAR] INVALID COMMAND" in captured.out
    assert "[EXIT]" in captured.out


def test_shell_exception_뜨면_안멈추고_메시지_띄우는지(monkeypatch, capsys, mocker):
    def broken_run_test(*args):
        raise Exception("boom")

    mock_driver = mocker.Mock()
    mock_handler = mocker.Mock()
    mock_handler_instance = mocker.Mock()
    mock_handler.return_value = mock_handler_instance
    mock_handler_instance.run_test.side_effect = broken_run_test

    CommandAction.registry["explode"] = mock_handler
    mocker.patch("ssd_clean_commit.src.shell.DummySSDDriver", return_value=mock_driver)

    simulate_shell(["explode", "exit"], monkeypatch)

    shell.main()

    captured = capsys.readouterr()
    assert "[ERROR] boom" in captured.out
