import pytest
from src.ssd_commands.ssd_read import ReadSSDCommand
from src.ssd_commands.ssd_command import InvalidArgumentException


@pytest.fixture
def mock_file_manager(mocker):
    return mocker.Mock()


@pytest.fixture
def mock_command_buffer(mocker):
    return mocker.Mock()


def test_read_command_fast_read에_성공하면_받은값을_SSDFileManager에_넘긴다(mock_file_manager, mock_command_buffer):
    mock_command_buffer.fast_read.return_value = "0xA1B2C3D4"
    command = ReadSSDCommand(mock_file_manager, mock_command_buffer, "10")

    command.execute()

    mock_file_manager.write_output.assert_called_once_with("0xA1B2C3D4")
    mock_file_manager.read.assert_not_called()
    mock_file_manager.error.assert_not_called()


def test_read_command_buffer에_없는경우_SSDFileManager로_read(mock_file_manager, mock_command_buffer):
    mock_command_buffer.fast_read.return_value = None
    mock_file_manager.read.return_value = "0x12345678"

    command = ReadSSDCommand(mock_file_manager, mock_command_buffer, "5")
    command.execute()

    mock_file_manager.read.assert_called_once_with(5)
    mock_file_manager.error.assert_not_called()


def test_read_command_arguement_잘못된_경우_SSDFileManager의_error를_호출한다(mock_file_manager, mock_command_buffer):
    command = ReadSSDCommand(mock_file_manager, mock_command_buffer, "abc")

    command.execute()

    mock_file_manager.read.assert_not_called()
    mock_file_manager.write_output.assert_not_called()
    mock_file_manager.error.assert_called_once()