import pytest

from src.read_command import ReadCommand
from src.ssd import VirtualSSD


def test_read_command_성공(mocker):
    mock_ssd = mocker.Mock(spec=VirtualSSD)
    test_address = 3
    test_value = "0x00000000"
    mock_ssd.read.return_value = test_value

    read_cmd = ReadCommand(mock_ssd, test_address)
    read_value = read_cmd.run()

    mock_ssd.read.assert_called_once()
    assert read_value == f'LBA {test_address}: {test_value}'


def test_read_command_유효성체크_LBA에러(mocker):
    mock_ssd = mocker.Mock(spec=VirtualSSD)
    test_address = 100

    read_cmd = ReadCommand(mock_ssd, test_address)

    with pytest.raises(ValueError):
        read_cmd.run()
    mock_ssd.read.assert_not_called()
