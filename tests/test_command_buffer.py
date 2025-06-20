import pytest
from pytest_mock import MockerFixture
from pathlib import Path

from src.command_buffer_handler import CommandBufferHandler
from src.command_buffer_data import ERASE, WRITE, EMPTY, CommandBufferException, CommandBufferData


@pytest.fixture
def command_buffer():
    command_buffer = CommandBufferHandler()
    command_buffer.initialize()
    return command_buffer


def test_initialize_성공(command_buffer):
    assert command_buffer.command_buffers == [CommandBufferData(order=1, command_type=EMPTY, lba=-1, value='', size=-1),
                                              CommandBufferData(order=2, command_type=EMPTY, lba=-1, value='', size=-1),
                                              CommandBufferData(order=3, command_type=EMPTY, lba=-1, value='', size=-1),
                                              CommandBufferData(order=4, command_type=EMPTY, lba=-1, value='', size=-1),
                                              CommandBufferData(order=5, command_type=EMPTY, lba=-1, value='', size=-1)]


def test_command_buffers_객체_생성_성공_파일_없는_상태():
    files_in_dir = [file for file in Path("../buffer").iterdir() if file.is_file()]
    for file in files_in_dir:
        file.unlink(missing_ok=True)

    command_buffer = CommandBufferHandler()
    command_buffer.initialize()

    assert command_buffer.command_buffers == [CommandBufferData(order=1, command_type=EMPTY, lba=-1, value='', size=-1),
                                              CommandBufferData(order=2, command_type=EMPTY, lba=-1, value='', size=-1),
                                              CommandBufferData(order=3, command_type=EMPTY, lba=-1, value='', size=-1),
                                              CommandBufferData(order=4, command_type=EMPTY, lba=-1, value='', size=-1),
                                              CommandBufferData(order=5, command_type=EMPTY, lba=-1, value='', size=-1)]


def test_command_buffers_객체_생성_성공_initialize_없는_상태(command_buffer):
    command_buffer.append(CommandBufferData(command_type=ERASE, lba=3, size=1))

    new_command_buffer = CommandBufferHandler()

    assert new_command_buffer.read_all() == [CommandBufferData(order=1, command_type=ERASE, lba=3, value='', size=1),
                                             CommandBufferData(order=2, command_type=EMPTY, lba=-1, value='', size=-1),
                                             CommandBufferData(order=3, command_type=EMPTY, lba=-1, value='', size=-1),
                                             CommandBufferData(order=4, command_type=EMPTY, lba=-1, value='', size=-1),
                                             CommandBufferData(order=5, command_type=EMPTY, lba=-1, value='', size=-1)]


def test_command_buffers_객체_생성_성공(command_buffer):
    assert command_buffer.command_buffers == [CommandBufferData(order=1, command_type=EMPTY, lba=-1, value='', size=-1),
                                              CommandBufferData(order=2, command_type=EMPTY, lba=-1, value='', size=-1),
                                              CommandBufferData(order=3, command_type=EMPTY, lba=-1, value='', size=-1),
                                              CommandBufferData(order=4, command_type=EMPTY, lba=-1, value='', size=-1),
                                              CommandBufferData(order=5, command_type=EMPTY, lba=-1, value='', size=-1)]


def test_fast_read_W에_값이_있을_때(command_buffer):
    command_buffer.append(CommandBufferData(command_type=WRITE, lba=3, value='0x00000001'))
    assert command_buffer.fast_read(3) == '0x00000001'


def test_fast_Read_E에_값이_있을_때(command_buffer):
    command_buffer.append(CommandBufferData(command_type=ERASE, lba=3, size=1))
    assert command_buffer.fast_read(3) == '0x00000000'


def test_fast_Read_값이_없을_때(command_buffer):
    command_buffer.append(CommandBufferData(command_type=ERASE, lba=3, size=1))
    assert command_buffer.fast_read(4) is None


def test_command_buffers_fast_read_성공_파일_없는_상태():
    files_in_dir = [file for file in Path("../buffer").iterdir() if file.is_file()]
    for file in files_in_dir:
        file.unlink(missing_ok=True)

    command_buffer = CommandBufferHandler()

    assert command_buffer.command_buffers == [CommandBufferData(order=1, command_type=EMPTY, lba=-1, value='', size=-1),
                                              CommandBufferData(order=2, command_type=EMPTY, lba=-1, value='', size=-1),
                                              CommandBufferData(order=3, command_type=EMPTY, lba=-1, value='', size=-1),
                                              CommandBufferData(order=4, command_type=EMPTY, lba=-1, value='', size=-1),
                                              CommandBufferData(order=5, command_type=EMPTY, lba=-1, value='', size=-1)]


def test_버퍼에_빈_값이_존재할_때_append_성공(command_buffer):
    command_buffer.append(CommandBufferData(command_type=WRITE, lba=3, value='0x00000001'))
    assert command_buffer.read_all() == [CommandBufferData(order=1, command_type=WRITE, lba=3, value='0x00000001', size=-1),
                                         CommandBufferData(order=2, command_type=EMPTY, lba=-1, value='', size=-1),
                                         CommandBufferData(order=3, command_type=EMPTY, lba=-1, value='', size=-1),
                                         CommandBufferData(order=4, command_type=EMPTY, lba=-1, value='', size=-1),
                                         CommandBufferData(order=5, command_type=EMPTY, lba=-1, value='', size=-1)]


def test_버퍼에_빈_값이_없을_때_failed(command_buffer):
    command_buffer.append(CommandBufferData(command_type=WRITE, lba=3, value='0x00000001'))
    command_buffer.append(CommandBufferData(command_type=WRITE, lba=4, value='0x00000002'))
    command_buffer.append(CommandBufferData(command_type=WRITE, lba=5, value='0x00000003'))
    command_buffer.append(CommandBufferData(command_type=WRITE, lba=6, value='0x00000004'))
    command_buffer.append(CommandBufferData(command_type=WRITE, lba=7, value='0x00000005'))

    with pytest.raises(CommandBufferException):
        command_buffer.append(CommandBufferData(command_type=WRITE, lba=8, value='0x00000006'))


def test_ignore_command_처리_case1(command_buffer):
    command_buffer.append(CommandBufferData(command_type=ERASE, lba=18, size=3))
    command_buffer.append(CommandBufferData(command_type=WRITE, lba=21, value='0x12341234'))
    command_buffer.append(CommandBufferData(command_type=ERASE, lba=18, size=5))

    assert command_buffer.read_all() == [CommandBufferData(order=1, command_type=ERASE, lba=18, value='', size=5),
                                         CommandBufferData(order=2, command_type=EMPTY, lba=-1, value='', size=-1),
                                         CommandBufferData(order=3, command_type=EMPTY, lba=-1, value='', size=-1),
                                         CommandBufferData(order=4, command_type=EMPTY, lba=-1, value='', size=-1),
                                         CommandBufferData(order=5, command_type=EMPTY, lba=-1, value='', size=-1)]


def test_ignore_command_처리_case2(command_buffer):
    command_buffer.append(CommandBufferData(command_type=ERASE, lba=1, size=2))
    command_buffer.append(CommandBufferData(command_type=WRITE, lba=1, value='0x12341234'))
    command_buffer.append(CommandBufferData(command_type=WRITE, lba=2, value='0x12341234'))

    assert command_buffer.read_all() == [CommandBufferData(order=1, command_type=WRITE, lba=1, value='0x12341234', size=-1),
                                         CommandBufferData(order=2, command_type=WRITE, lba=2, value='0x12341234', size=-1),
                                         CommandBufferData(order=3, command_type=EMPTY, lba=-1, value='', size=-1),
                                         CommandBufferData(order=4, command_type=EMPTY, lba=-1, value='', size=-1),
                                         CommandBufferData(order=5, command_type=EMPTY, lba=-1, value='', size=-1)]


def test_ignore_command_처리_case3(command_buffer):
    command_buffer.append(CommandBufferData(command_type=ERASE, lba=1, size=3))
    command_buffer.append(CommandBufferData(command_type=WRITE, lba=2, value='0x12341234'))

    assert command_buffer.read_all() == [CommandBufferData(order=1, command_type=ERASE, lba=1, value='', size=3),
                                         CommandBufferData(order=2, command_type=WRITE, lba=2, value='0x12341234', size=-1),
                                         CommandBufferData(order=3, command_type=EMPTY, lba=-1, value='', size=-1),
                                         CommandBufferData(order=4, command_type=EMPTY, lba=-1, value='', size=-1),
                                         CommandBufferData(order=5, command_type=EMPTY, lba=-1, value='', size=-1)]


def test_merge_erase_처리_case1(command_buffer):
    command_buffer.append(CommandBufferData(command_type=WRITE, lba=20, value='0xABCDABCD'))
    command_buffer.append(CommandBufferData(command_type=ERASE, lba=10, size=4))
    command_buffer.append(CommandBufferData(command_type=ERASE, lba=12, size=3))

    assert command_buffer.read_all() == [CommandBufferData(order=1, command_type=WRITE, lba=20, value='0xABCDABCD', size=-1),
                                         CommandBufferData(order=2, command_type=ERASE, lba=10, value='', size=5),
                                         CommandBufferData(order=3, command_type=EMPTY, lba=-1, value='', size=-1),
                                         CommandBufferData(order=4, command_type=EMPTY, lba=-1, value='', size=-1),
                                         CommandBufferData(order=5, command_type=EMPTY, lba=-1, value='', size=-1)]


def test_merge_erase_처리_case2(command_buffer):
    command_buffer.append(CommandBufferData(command_type=ERASE, lba=0, size=7))
    command_buffer.append(CommandBufferData(command_type=ERASE, lba=7, size=7))

    assert command_buffer.read_all() == [CommandBufferData(order=1, command_type=ERASE, lba=0, value='', size=7),
                                         CommandBufferData(order=2, command_type=ERASE, lba=7, value='', size=7),
                                         CommandBufferData(order=3, command_type=EMPTY, lba=-1, value='', size=-1),
                                         CommandBufferData(order=4, command_type=EMPTY, lba=-1, value='', size=-1),
                                         CommandBufferData(order=5, command_type=EMPTY, lba=-1, value='', size=-1)]


def test_merge_erase_처리_case3(command_buffer):
    command_buffer.append(CommandBufferData(command_type=ERASE, lba=0, size=7))
    command_buffer.append(CommandBufferData(command_type=ERASE, lba=7, size=7))
    command_buffer.append(CommandBufferData(command_type=ERASE, lba=14, size=4))

    assert command_buffer.read_all() == [CommandBufferData(order=1, command_type=ERASE, lba=0, value='', size=10),
                                         CommandBufferData(order=2, command_type=ERASE, lba=10, value='', size=8),
                                         CommandBufferData(order=3, command_type=EMPTY, lba=-1, value='', size=-1),
                                         CommandBufferData(order=4, command_type=EMPTY, lba=-1, value='', size=-1),
                                         CommandBufferData(order=5, command_type=EMPTY, lba=-1, value='', size=-1)]


def test_ignore_command와_merge_erase_동시_처리(command_buffer):
    command_buffer.append(CommandBufferData(command_type=WRITE, lba=15, size=0xABCDABCD))
    command_buffer.append(CommandBufferData(command_type=ERASE, lba=0, size=7))
    command_buffer.append(CommandBufferData(command_type=ERASE, lba=7, size=7))
    command_buffer.append(CommandBufferData(command_type=ERASE, lba=14, size=4))

    assert command_buffer.read_all() == [CommandBufferData(order=1, command_type=ERASE, lba=0, value='', size=10),
                                         CommandBufferData(order=2, command_type=ERASE, lba=10, value='', size=8),
                                         CommandBufferData(order=3, command_type=EMPTY, lba=-1, value='', size=-1),
                                         CommandBufferData(order=4, command_type=EMPTY, lba=-1, value='', size=-1),
                                         CommandBufferData(order=5, command_type=EMPTY, lba=-1, value='', size=-1)]


def test_ignore_command와_merge_erase_동시_처리_case2(command_buffer):
    command_buffer.append(CommandBufferData(command_type=ERASE, lba=1, size=3))
    command_buffer.append(CommandBufferData(command_type=WRITE, lba=2, value='0x12341234'))
    command_buffer.append(CommandBufferData(command_type=ERASE, lba=4, size=5))

    assert command_buffer.read_all() == [CommandBufferData(order=1, command_type=ERASE, lba=1, value='', size=8),
                                         CommandBufferData(order=2, command_type=WRITE, lba=2, value='0x12341234', size=-1),
                                         CommandBufferData(order=3, command_type=EMPTY, lba=-1, value='', size=-1),
                                         CommandBufferData(order=4, command_type=EMPTY, lba=-1, value='', size=-1),
                                         CommandBufferData(order=5, command_type=EMPTY, lba=-1, value='', size=-1)]
