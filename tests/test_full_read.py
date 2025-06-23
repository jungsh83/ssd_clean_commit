import pytest

from src.shell_commands.shell_command_action import InvalidArgumentException
from src.shell_commands.action.full_read import FullReadShellCommand
from src.ssd_file_manager import SSDFileManager
from src.data_dict import *


@pytest.fixture
def ssd_driver(mocker):
    driver = mocker.Mock()
    driver.LBA_COUNT = LBA_COUNT  # 100
    driver.read.side_effect = lambda lba: f"0x{lba:08X}"
    return driver


def test_fullread_100줄_출력확인(ssd_driver):
    result = FullReadShellCommand(ssd_driver).run()
    assert len(result.splitlines()) == LBA_COUNT


def test_fullread_첫줄_LBA0_값확인(ssd_driver):
    result = FullReadShellCommand(ssd_driver).run()
    first = result.splitlines()[0]
    assert first == "0 0x00000000"


def test_fullread_마지막줄_LBA99_값확인(ssd_driver):
    result = FullReadShellCommand(ssd_driver).run()
    last = result.splitlines()[-1]

    indent = " " * 11  # 줄 앞에 들어가는 11칸 공백
    expected = f"{indent}{LBA_COUNT - 1} 0x{LBA_COUNT - 1:08X}"
    assert last == expected  # '           99 0x00000063'


def test_fullread_유효성범위검사(ssd_driver):
    with pytest.raises(InvalidArgumentException):
        FullReadShellCommand(ssd_driver, "dummy").run()
