import pytest

from src.commands.command_action import InvalidArgumentException
from src.commands.read import ReadCommand
from src.ssd import VirtualSSD


@pytest.fixture
def mock_ssd(mocker):
    mock_ssd = mocker.Mock(spec=VirtualSSD)
    return mock_ssd


@pytest.mark.parametrize('test_address, test_value', [(3, "0x00000000"), (99, "0xABCDEF00"), (50, "0x12345678")])
def test_read_command_성공(test_address, test_value, mock_ssd):
    mock_ssd.read.return_value = test_value

    read_cmd = ReadCommand(mock_ssd, test_address)
    read_value = read_cmd.run()

    mock_ssd.read.assert_called_once()
    assert read_value == f'LBA {test_address}: {test_value}'


@pytest.mark.parametrize('test_address, test_value', [(1, "0x00000000"), (100, "0x00000000"),
                                                      (0.1, "0x00000000"), (-1, "0x00000000"),
                                                      ('c', "0x00000000")])
def test_read_command_유효성체크_Param개수_초과(test_address, test_value, mock_ssd):
    read_cmd = ReadCommand(mock_ssd, test_address, test_value)

    with pytest.raises(InvalidArgumentException):
        read_cmd.run()
    mock_ssd.read.assert_not_called()


def test_read_command_유효성체크_Param개수_부족(mock_ssd):
    read_cmd = ReadCommand(mock_ssd)

    with pytest.raises(InvalidArgumentException):
        read_cmd.run()
    mock_ssd.read.assert_not_called()
