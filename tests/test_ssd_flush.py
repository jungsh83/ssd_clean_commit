import pytest

from src.command_buffer import CommandBuffer
from src.ssd_commands.ssd_flush import SSDFlushCommand
from src.ssd_file_manager import SSDFileManager


@pytest.fixture
def mock_buffer_and_manager(mocker):
    return mocker.Mock(spec=CommandBuffer), mocker.Mock(spec=SSDFileManager)


@pytest.mark.skip
def test_flush_성공(mock_buffer_and_manager):
    mock_cmd_buffer, mock_file_manager = mock_buffer_and_manager

    ssd_flush_cmd = SSDFlushCommand(mock_file_manager, mock_cmd_buffer)
    ssd_flush_cmd.run()


def test_flush_파라미터_초과(mock_buffer_and_manager):
    error_arg = 'test'
    mock_cmd_buffer, mock_file_manager = mock_buffer_and_manager
    ssd_flush_cmd = SSDFlushCommand(mock_file_manager, mock_cmd_buffer, error_arg)

    assert not ssd_flush_cmd.validate()
