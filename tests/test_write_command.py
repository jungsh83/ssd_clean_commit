import pytest

from src.ssd import VirtualSSD
from src.write_command import WriteCommand


@pytest.fixture
def mock_ssd(mocker):
    mock_ssd = mocker.Mock(spec=VirtualSSD)
    return mock_ssd


@pytest.mark.parametrize('test_address', [0, 15, 99])
def test_write_command_성공(test_address, mock_ssd):
    test_value = "0x12345678"

    write_cmd = WriteCommand(mock_ssd, test_address, test_value)
    write_cmd.run()

    mock_ssd.write.assert_called_once()


@pytest.mark.parametrize('test_address', [-1, 200, 'c'])
def test_write_command_유효성검사_LBA오류(test_address, mock_ssd):
    test_value = "0x12345678"

    write_cmd = WriteCommand(mock_ssd, test_address, test_value)

    with pytest.raises(ValueError, match=WriteCommand.ERROR_UNVALIDATED):
        write_cmd.run()

    assert write_cmd.validate() is False
    mock_ssd.write.assert_not_called()


@pytest.mark.parametrize('test_value', ['0x1234567Z', '0x123456Z8', '0x12345Z78', '0x1234Z678',
                                        '0x123Z5678', '0x12Z45678', '0x1Z345678', '0xZ2345678',
                                        0.1, 'c', -1, '0x1111', '0x11111'])
def test_write_command_유효성검사_Value오류(test_value, mock_ssd):
    test_address = 0

    write_cmd = WriteCommand(mock_ssd, test_address, test_value)

    with pytest.raises(ValueError, match=WriteCommand.ERROR_UNVALIDATED):
        write_cmd.run()

    assert write_cmd.validate() is False
    mock_ssd.write.assert_not_called()


@pytest.mark.parametrize('test_value, error_param', [('0x1234567Z', -1), ('0x123456Z8', 'c'),
                                                     ('0x12345Z78', 1), ('0x1234Z678', 100),
                                                     ('0x123Z5678', 0.1), ('0x12Z45678', 123),
                                                     ('0x1Z345678', 1), ('0xZ2345678', 0)])
def test_write_command_유효성검사_Param개수_초과(test_value, error_param, mock_ssd):
    test_address = 0

    write_cmd = WriteCommand(mock_ssd, test_address, test_value, error_param)

    with pytest.raises(ValueError, match=WriteCommand.ERROR_UNVALIDATED):
        write_cmd.run()

    assert write_cmd.validate() is False
    mock_ssd.write.assert_not_called()


def test_write_command_유효성검사_Param개수_부족(mock_ssd):
    write_cmd = WriteCommand(mock_ssd)

    with pytest.raises(ValueError, match=WriteCommand.ERROR_UNVALIDATED):
        write_cmd.run()

    assert write_cmd.validate() is False
    mock_ssd.write.assert_not_called()
