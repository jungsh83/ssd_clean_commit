import pytest

from src.shell_commands.shell_command import InvalidArgumentException
from src.shell_commands.action.full_write import FullWriteShellCommand
from src.ssd_file_manager import SSDFileManager
from src.ssd_driver import SSDDriver
from src.data_dict import *

@pytest.fixture
def mock_ssd_driver(mocker):
    return mocker.Mock(spec=SSDDriver)


def test_full_write_command_성공(mock_ssd_driver):
    test_value = '0x12345678'

    full_write_cmd = FullWriteShellCommand(mock_ssd_driver, test_value)

    full_write_cmd.execute()

    assert mock_ssd_driver.write.call_count == LBA_COUNT


def test_full_write_command_유효성검사_Param개수_부족(mock_ssd_driver):
    full_write_cmd = FullWriteShellCommand(mock_ssd_driver)

    with pytest.raises(InvalidArgumentException):
        full_write_cmd.execute()

    assert not full_write_cmd.validate()
    mock_ssd_driver.write.assert_not_called()


@pytest.mark.parametrize('test_value, error_param', [('0x1234567Z', -1), ('0x123456Z8', 'c'),
                                                     ('0x12345Z78', 1), ('0x1234Z678', 100),
                                                     ('0x123Z5678', 0.1), ('0x12Z45678', 123),
                                                     ('0x1Z345678', 1), ('0xZ2345678', 0)])
def test_full_write_command_유효성검사_Param개수_초과(test_value, error_param, mock_ssd_driver):
    full_write_cmd = FullWriteShellCommand(mock_ssd_driver, test_value, error_param)

    with pytest.raises(InvalidArgumentException):
        full_write_cmd.execute()

    assert not full_write_cmd.validate()
    mock_ssd_driver.write.assert_not_called()
