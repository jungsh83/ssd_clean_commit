import pytest

from src.full_write_command import FullWriteCommand
from src.ssd import VirtualSSD


def test_full_write_command_성공(mocker):
    mock_ssd = mocker.Mock(spec=VirtualSSD)
    test_value = '0x12345678'

    full_write_cmd = FullWriteCommand(mock_ssd, test_value)

    full_write_cmd.run()

    assert mock_ssd.write.call_count == 100


def test_full_write_command_유효성검사_value_type에러(mocker):
    mock_ssd = mocker.Mock(spec=VirtualSSD)
    test_value = 3

    full_write_cmd = FullWriteCommand(mock_ssd, test_value)

    with pytest.raises(ValueError):
        full_write_cmd.run()

    assert full_write_cmd.validate() is False
    mock_ssd.write.assert_not_called()


def test_full_write_command_유효성검사_value_값에러(mocker):
    mock_ssd = mocker.Mock(spec=VirtualSSD)
    test_value = '0x1234567Z'

    full_write_cmd = FullWriteCommand(mock_ssd, test_value)

    with pytest.raises(ValueError):
        full_write_cmd.run()

    assert full_write_cmd.validate() is False
    mock_ssd.write.assert_not_called()
