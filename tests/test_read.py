import pytest

from src.shell_commands.shell_command_action import InvalidArgumentException
from src.shell_commands.action.read import ReadShellCommand
from src.ssd_driver import SSDDriver


@pytest.fixture
def mock_ssd_driver(mocker):
    return mocker.Mock(spec=SSDDriver)


@pytest.mark.parametrize('test_address, test_value', [(3, "0x00000000"), (99, "0xABCDEF00"), (50, "0x12345678")])
def test_read_command_성공(test_address, test_value, mock_ssd_driver):
    mock_ssd_driver.read.return_value = test_value

    read_cmd = ReadShellCommand(mock_ssd_driver, test_address)
    read_value = read_cmd.run()

    mock_ssd_driver.read.assert_called_once()
    assert read_value == ReadShellCommand.print_output(test_address, test_value)


@pytest.mark.parametrize('test_address, test_value', [(1, "0x00000000"), (100, "0x00000000"),
                                                      (0.1, "0x00000000"), (-1, "0x00000000"),
                                                      ('c', "0x00000000")])
def test_read_command_유효성체크_Param개수_초과(test_address, test_value, mock_ssd_driver):
    read_cmd = ReadShellCommand(mock_ssd_driver, test_address, test_value)

    with pytest.raises(InvalidArgumentException):
        read_cmd.run()
    mock_ssd_driver.read.assert_not_called()


def test_read_command_유효성체크_Param개수_부족(mock_ssd_driver):
    read_cmd = ReadShellCommand(mock_ssd_driver)

    with pytest.raises(InvalidArgumentException):
        read_cmd.run()
    mock_ssd_driver.read.assert_not_called()
