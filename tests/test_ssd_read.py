import pytest
from ssd_read_command import ReadCommand
from ssd_command_action import InvalidArgumentException


@pytest.fixture
def mock_ssd_file_manager(mocker):
    return mocker.Mock()


@pytest.fixture
def mock_command_buffer(mocker):
    return mocker.Mock()


def test_readcommand_fast_read_사용되는경우(mock_ssd_file_manager, mock_command_buffer):
    mock_command_buffer.fast_read.return_value = "0xAABBCCDD"
    cmd = ReadCommand(mock_ssd_file_manager, mock_command_buffer, "5")

    result = cmd.run()

    mock_command_buffer.fast_read.assert_called_once_with(5)
    mock_ssd_file_manager.write_output.assert_called_once_with("0xAABBCCDD")
    assert result == "[READ] LBA 5 : 0xAABBCCDD"


def test_readcommand_ssdfilemanager_read_사용되는경우(mock_ssd_file_manager, mock_command_buffer):
    # fast_read가 None이면 read()로 fallback
    mock_command_buffer.fast_read.return_value = None
    mock_ssd_file_manager.read.return_value = "0x12345678"
    cmd = ReadCommand(mock_ssd_file_manager, mock_command_buffer, "7")

    result = cmd.run()

    mock_command_buffer.fast_read.assert_called_once_with(7)
    mock_ssd_file_manager.read.assert_called_once_with(7)
    assert result == "[READ] LBA 7 : 0x12345678"


@pytest.mark.parametrize("invalid_args", [
    [],                   # no args
    ["1", "2"],           # too many args
    ["notanumber"],       # not digit
    ["-1"],               # negative number (still digit but likely invalid in range)
])
def test_readcommand_invalid_arguments_raise(invalid_args, mock_ssd_file_manager, mock_command_buffer):
    cmd = ReadCommand(mock_ssd_file_manager, mock_command_buffer, *invalid_args)
    with pytest.raises(InvalidArgumentException):
        cmd.run()
