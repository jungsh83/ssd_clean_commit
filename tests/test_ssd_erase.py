import pytest
from src.ssd_commands.ssd_command_action import SSDCommand, InvalidArgumentException
from src.ssd_commands.ssd_erase_command import SSDCommandErase
from src.ssd_file_manager import SSDFileManager
from src.command_buffer.command_buffer_handler import CommandBufferHandler


@pytest.fixture
def get_filemanage_command_handler(mocker):
    file_manager = SSDFileManager()
    command_buffer_handler = CommandBufferHandler()
    return file_manager, command_buffer_handler


@pytest.mark.parametrize("lba, size, expected_erase_start, expected_erase_end", [
    (98, 2, 98, 99),
    (5, 1, 5, 5),
    (5, 10, 5, 14),
])
def test_erase_성공(get_filemanage_command_handler, lba, size, expected_erase_start, expected_erase_end):
    file_manager, command_buffer_handler = get_filemanage_command_handler
    cmd = SSDCommandErase(file_manager, command_buffer_handler, str(lba), str(size))

    cmd.run()

    # assert
    data = cmd._ssd_file_manager._load_nand()
    for i in range(expected_erase_start, expected_erase_end + 1):
        assert data[i] == cmd._ssd_file_manager.DEFAULT_VAL


@pytest.mark.parametrize("lba, size", [
    (50, -100),
    (85, 100),
    (100, 10),
    (-1, 10),
    ("가나다", 10),
    (5, "가다")
])
def test_erase_파라미터_유효성오류(get_filemanage_command_handler, lba, size):
    file_manager, command_buffer_handler = get_filemanage_command_handler
    cmd = SSDCommandErase(file_manager, command_buffer_handler, str(lba), str(size))

    with pytest.raises(InvalidArgumentException):
        cmd.run()
