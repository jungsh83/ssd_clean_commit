import pytest
from unittest.mock import MagicMock, patch
from src import ssd_file_manager
import ssd


@pytest.fixture(autouse=True)
def ssd_file_manager_초기화():
    ssd_file_manager.SSDFileManager._reset_instance()


@pytest.mark.parametrize("args,command_key", [
    (["R", "0"], "R"),
    (["W", "1", "0x12345678"], "W"),
    (["E", "10", "2"], "E"),
    (["F"], "F"),
])
def test_main_정상_명령어가_호출되면_해당_커맨드클래스를_실행한다(args, command_key):
    mock_cmd_class = MagicMock()
    mock_instance = mock_cmd_class.return_value

    with patch.dict(ssd.SSD_COMMANDS, {command_key: mock_cmd_class}):
        ssd.main(args)

    mock_cmd_class.assert_called_once()
    mock_instance.execute.assert_called_once()


def test_main_없는_명령어_입력시_ERROR를_출력한다(monkeypatch, capsys):
    monkeypatch.setattr(ssd_file_manager.SSDFileManager, 'error', lambda self: print("ERROR"))
    ssd.main(["X", "0"])
    captured = capsys.readouterr()
    assert "ERROR" in captured.out


def test_main_명령어가_비어있으면_ERROR를_출력한다(monkeypatch, capsys):
    monkeypatch.setattr(ssd_file_manager.SSDFileManager, 'error', lambda self: print("ERROR"))
    ssd.main([])
    captured = capsys.readouterr()
    assert "ERROR" in captured.out