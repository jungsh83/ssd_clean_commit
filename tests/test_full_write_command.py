import pytest

from src.full_write_command import FullWriteCommand
from src.ssd import VirtualSSD


def test_full_write_command_성공(mocker):
    mock_ssd = mocker.Mock(spec=VirtualSSD)
    test_value = '0x12345678'

    full_write_cmd = FullWriteCommand(mock_ssd, test_value)

    full_write_cmd.run()

    assert mock_ssd.write.call_count == 100


@pytest.mark.parametrize('test_value', ['0x1234567Z', '0x123456Z8', '0x12345Z78', '0x1234Z678',
                                        '0x123Z5678', '0x12Z45678', '0x1Z345678', '0xZ2345678',
                                        -3, 'c', 0.1])
def test_full_write_command_유효성검사_value_에러(test_value, mocker):
    mock_ssd = mocker.Mock(spec=VirtualSSD)

    full_write_cmd = FullWriteCommand(mock_ssd, test_value)

    with pytest.raises(ValueError):
        full_write_cmd.run()

    assert full_write_cmd.validate() is False
    mock_ssd.write.assert_not_called()


def test_full_write_command_유효성검사_Param개수_부족(mocker):
    mock_ssd = mocker.Mock(spec=VirtualSSD)

    full_write_cmd = FullWriteCommand(mock_ssd)

    with pytest.raises(ValueError):
        full_write_cmd.run()

    assert full_write_cmd.validate() is False
    mock_ssd.write.assert_not_called()
