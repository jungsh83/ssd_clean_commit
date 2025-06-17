import pytest

from src.ssd import VirtualSSD
from src.write_command import WriteCommand

def test_write_command_성공(mocker):
    mock_ssd = mocker.Mock(spec=VirtualSSD)
    test_address = 3
    test_value = "0x12345678"

    write_cmd = WriteCommand(mock_ssd, test_address, test_value)
    write_cmd.run()

    mock_ssd.write.assert_called_once()


@pytest.mark.parametrize('test_address', [-1, 200])
def test_write_command_유효성검사_LBA오류(test_address, mocker):
    mock_ssd = mocker.Mock(spec=VirtualSSD)
    test_value = "0x12345678"

    write_cmd = WriteCommand(mock_ssd, test_address, test_value)
    write_cmd.run()

    assert write_cmd.validate() is False
    mock_ssd.write.assert_not_called()
