import pytest

from src.command_buffer.command_buffer_data import CommandBufferData, WRITE, ERASE
from src.command_buffer.command_buffer_handler import CommandBufferHandler
from src.ssd_commands.ssd_flush import FlushSSDCommand
from src.ssd_file_manager import SSDFileManager


@pytest.fixture
def mock_buffer_and_manager(mocker):
    return mocker, mocker.Mock(spec=CommandBufferHandler), mocker.Mock(spec=SSDFileManager)


def test_flush_성공(mock_buffer_and_manager):
    mocker, mock_cmd_buffer, mock_file_manager = mock_buffer_and_manager

    def mock_buffer_data(cmd_type, lba, cmd_value):
        cmd_data = mocker.Mock(spec=CommandBufferData)
        cmd_data.order = 1
        cmd_data.command_type = cmd_type
        cmd_data.lba = lba
        cmd_data.value = cmd_value

        return cmd_data

    mock_cmd_buffer.command_buffers = [mock_buffer_data(WRITE, 0, "0x12345678"),
                                       mock_buffer_data(WRITE, 1, "0x12345678"),
                                       mock_buffer_data(WRITE, 2, "0x12345678"),
                                       mock_buffer_data(ERASE, 3, 5),
                                       mock_buffer_data(ERASE, 90, 10)]

    ssd_flush_cmd = FlushSSDCommand(mock_file_manager, mock_cmd_buffer)
    ret = ssd_flush_cmd.run()

    assert ret == "PASS"
    assert mock_file_manager.write.call_count == 3
    assert mock_file_manager.erase.call_count == 2
    mock_cmd_buffer.initialize.assert_called_once()


def test_flush_파라미터_초과(mock_buffer_and_manager):
    error_arg = 'test'
    mocker, mock_cmd_buffer, mock_file_manager = mock_buffer_and_manager

    ssd_flush_cmd = FlushSSDCommand(mock_file_manager, mock_cmd_buffer, error_arg)
    ret = ssd_flush_cmd.run()

    assert ret == "FAIL"
    assert not ssd_flush_cmd.validate()
    mock_file_manager.error.assert_called_once()
