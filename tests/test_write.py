import pytest

from src.shell_commands.shell_command_action import InvalidArgumentException
from src.shell_commands.action.write import WriteShellCommand
from src.ssd_driver import SSDDriver


@pytest.fixture
def mock_ssd_driver(mocker):
    return mocker.Mock(spec=SSDDriver)


@pytest.mark.parametrize('test_address', [0, 15, 99])
def test_write_command_성공(test_address, mock_ssd_driver):
    test_value = "0x12345678"

    write_cmd = WriteShellCommand(mock_ssd_driver, test_address, test_value)
    write_cmd.run()

    mock_ssd_driver.write.assert_called_once()


@pytest.mark.parametrize('test_value, error_param', [('0x1234567Z', -1), ('0x123456Z8', 'c'),
                                                     ('0x12345Z78', 1), ('0x1234Z678', 100),
                                                     ('0x123Z5678', 0.1), ('0x12Z45678', 123),
                                                     ('0x1Z345678', 1), ('0xZ2345678', 0)])
def test_write_command_유효성검사_Param개수_초과(test_value, error_param, mock_ssd_driver):
    test_address = 0

    write_cmd = WriteShellCommand(mock_ssd_driver, test_address, test_value, error_param)

    with pytest.raises(InvalidArgumentException):
        write_cmd.run()

    assert not write_cmd.validate()
    mock_ssd_driver.write.assert_not_called()


def test_write_command_유효성검사_Param개수_부족(mock_ssd_driver):
    write_cmd = WriteShellCommand(mock_ssd_driver)

    with pytest.raises(InvalidArgumentException):
        write_cmd.run()

    assert not write_cmd.validate()
    mock_ssd_driver.write.assert_not_called()
