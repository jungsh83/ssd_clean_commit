import pytest
from pytest_mock import MockerFixture
from pathlib import Path

from src.command_buffer import CommandBuffer, Command, CommandBufferException


@pytest.fixture
def command_buffer():
    command_buffer = CommandBuffer()
    command_buffer.initialize()
    return command_buffer


def test_initialize_성공(command_buffer):
    assert command_buffer.command_buffers == [Command(order=1, command_type='I', lba=-1, value='', size=-1),
                                              Command(order=2, command_type='I', lba=-1, value='', size=-1),
                                              Command(order=3, command_type='I', lba=-1, value='', size=-1),
                                              Command(order=4, command_type='I', lba=-1, value='', size=-1),
                                              Command(order=5, command_type='I', lba=-1, value='', size=-1)]


def test_command_buffers_객체_생성_성공_파일_없는_상태():
    files_in_dir = [file for file in Path("../buffer").iterdir() if file.is_file()]
    for file in files_in_dir:
        file.unlink(missing_ok=True)

    command_buffer = CommandBuffer()
    command_buffer.initialize()

    assert command_buffer.command_buffers == [Command(order=1, command_type='I', lba=-1, value='', size=-1),
                                              Command(order=2, command_type='I', lba=-1, value='', size=-1),
                                              Command(order=3, command_type='I', lba=-1, value='', size=-1),
                                              Command(order=4, command_type='I', lba=-1, value='', size=-1),
                                              Command(order=5, command_type='I', lba=-1, value='', size=-1)]


def test_command_buffers_객체_생성_성공_initialize_없는_상태(command_buffer):
    command_buffer.append(Command(command_type='E', lba=3, size=1))

    new_command_buffer = CommandBuffer()

    assert new_command_buffer.read_all() == [Command(order=1, command_type='E', lba=3, value='', size=1),
                                             Command(order=2, command_type='I', lba=-1, value='', size=-1),
                                             Command(order=3, command_type='I', lba=-1, value='', size=-1),
                                             Command(order=4, command_type='I', lba=-1, value='', size=-1),
                                             Command(order=5, command_type='I', lba=-1, value='', size=-1)]


def test_command_buffers_객체_생성_성공(command_buffer):
    assert command_buffer.command_buffers == [Command(order=1, command_type='I', lba=-1, value='', size=-1),
                                              Command(order=2, command_type='I', lba=-1, value='', size=-1),
                                              Command(order=3, command_type='I', lba=-1, value='', size=-1),
                                              Command(order=4, command_type='I', lba=-1, value='', size=-1),
                                              Command(order=5, command_type='I', lba=-1, value='', size=-1)]


def test_fast_read_W에_값이_있을_때(command_buffer):
    command_buffer.append(Command(command_type='W', lba=3, value='0x00000001'))
    assert command_buffer.fast_read(3) == '0x00000001'


def test_fast_Read_E에_값이_있을_때(command_buffer):
    command_buffer.append(Command(command_type='E', lba=3, size=1))
    assert command_buffer.fast_read(3) == '0x00000000'


def test_fast_Read_값이_없을_때(command_buffer):
    command_buffer.append(Command(command_type='E', lba=3, size=1))
    assert command_buffer.fast_read(4) is None


def test_command_buffers_fast_read_성공_파일_없는_상태():
    files_in_dir = [file for file in Path("../buffer").iterdir() if file.is_file()]
    for file in files_in_dir:
        file.unlink(missing_ok=True)

    command_buffer = CommandBuffer()

    assert command_buffer.command_buffers == [Command(order=1, command_type='I', lba=-1, value='', size=-1),
                                              Command(order=2, command_type='I', lba=-1, value='', size=-1),
                                              Command(order=3, command_type='I', lba=-1, value='', size=-1),
                                              Command(order=4, command_type='I', lba=-1, value='', size=-1),
                                              Command(order=5, command_type='I', lba=-1, value='', size=-1)]


def test_버퍼에_빈_값이_존재할_때_append_성공(command_buffer):
    command_buffer.append(Command(command_type='W', lba=3, value='0x00000001'))
    assert command_buffer.read_all() == [Command(order=1, command_type='W', lba=3, value='0x00000001', size=-1),
                                         Command(order=2, command_type='I', lba=-1, value='', size=-1),
                                         Command(order=3, command_type='I', lba=-1, value='', size=-1),
                                         Command(order=4, command_type='I', lba=-1, value='', size=-1),
                                         Command(order=5, command_type='I', lba=-1, value='', size=-1)]


def test_버퍼에_빈_값이_없을_때_failed(command_buffer):
    command_buffer.append(Command(command_type='W', lba=3, value='0x00000001'))
    command_buffer.append(Command(command_type='W', lba=3, value='0x00000001'))
    command_buffer.append(Command(command_type='W', lba=3, value='0x00000001'))
    command_buffer.append(Command(command_type='W', lba=3, value='0x00000001'))
    command_buffer.append(Command(command_type='W', lba=3, value='0x00000001'))

    with pytest.raises(CommandBufferException):
        command_buffer.append(Command(command_type='W', lba=3, value='0x00000001'))

