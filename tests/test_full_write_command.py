import pytest

from src.full_write_command import FullWriteCommand
from src.ssd import VirtualSSD


def test_full_write_command_성공(mocker):
    mock_ssd = mocker.Mock(spec=VirtualSSD)
    test_value = '0x12345678'

    full_write_cmd = FullWriteCommand(mock_ssd, test_value)

    full_write_cmd.run()

    assert mock_ssd.write.call_count == 100

