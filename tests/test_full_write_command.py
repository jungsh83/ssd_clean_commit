import pytest

from src.full_write_command import FullWriteCommand
from src.ssd import VirtualSSD


@pytest.fixture
def mock_ssd(mocker):
    return mocker.Mock(spec=VirtualSSD)


def test_full_write_command_성공(mock_ssd):
    test_value = '0x12345678'

    full_write_cmd = FullWriteCommand(mock_ssd, test_value)

    full_write_cmd.run()

    assert mock_ssd.write.call_count == 100


@pytest.mark.parametrize('test_value', ['0x1234567Z', '0x123456Z8', '0x12345Z78', '0x1234Z678',
                                        '0x123Z5678', '0x12Z45678', '0x1Z345678', '0xZ2345678',
                                        -3, 'c', 0.1, '0x1111', '0x123456', '1234567890', 'AAAAABBBBB'])
def test_full_write_command_유효성검사_value_에러(test_value, mock_ssd):
    full_write_cmd = FullWriteCommand(mock_ssd, test_value)

    with pytest.raises(ValueError, match=FullWriteCommand.ERROR_UNVALIDATED):
        full_write_cmd.run()

    assert not full_write_cmd.validate()
    mock_ssd.write.assert_not_called()


def test_full_write_command_유효성검사_Param개수_부족(mock_ssd):
    full_write_cmd = FullWriteCommand(mock_ssd)

    with pytest.raises(ValueError, match=FullWriteCommand.ERROR_UNVALIDATED):
        full_write_cmd.run()

    assert not full_write_cmd.validate()
    mock_ssd.write.assert_not_called()


@pytest.mark.parametrize('test_value, error_param', [('0x1234567Z', -1), ('0x123456Z8', 'c'),
                                                     ('0x12345Z78', 1), ('0x1234Z678', 100),
                                                     ('0x123Z5678', 0.1), ('0x12Z45678', 123),
                                                     ('0x1Z345678', 1), ('0xZ2345678', 0)])
def test_full_write_command_유효성검사_Param개수_초과(test_value, error_param, mock_ssd):
    full_write_cmd = FullWriteCommand(mock_ssd, test_value, error_param)

    with pytest.raises(ValueError, match=FullWriteCommand.ERROR_UNVALIDATED):
        full_write_cmd.run()

    assert not full_write_cmd.validate()
    mock_ssd.write.assert_not_called()
