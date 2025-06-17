from src.read_command import ReadCommand
from src.ssd import VirtualSSD


def test_read_command_성공(mocker):
    mock_ssd = mocker.Mock(spec=VirtualSSD)
    test_address = 3
    test_value = "0x00000000"
    mock_ssd.read.return_value = test_value

    read_cmd = ReadCommand(mock_ssd, test_address)
    read_value = read_cmd.run()

    mock_ssd.read.assert_called_once()
    assert read_value == test_value
