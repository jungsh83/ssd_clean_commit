import pytest
from pytest_mock import MockFixture

from src.ssd_file_manager import SSDFileManager
from src.command_buffer import CommandBuffer, Command
from src.ssd_commands.ssd_write import WriteCommandAction


@pytest.fixture
def ssd_file_manager():
    return SSDFileManager()


@pytest.fixture
def command_buffer(mocker: MockFixture):
    mock_method = mocker.patch("src.command_buffer.CommandBuffer.read_all")
    mock_method.side_effect = mk_read_all

    obj = CommandBuffer()
    return obj


def mk_read_all():
    return [
        Command(order=1, command_type="W", lba=0, value="0x00000000"),
        Command(order=1, command_type="W", lba=1, value="0x00000001"),
        Command(order=1, command_type="W", lba=2, value="0x00000002"),
        Command(order=1, command_type="W", lba=3, value="0x00000003"),
        Command(order=1, command_type="W", lba=4, value="0x00000004"),
    ]


@pytest.mark.parametrize(
    "lba, value",
    [(0, "0x00000001"), (33, "0x00000002")]
)
def test_validate_성공(ssd_file_manager, command_buffer, lba, value):
    sut = WriteCommandAction(ssd_file_manager, command_buffer, lba, value)
    assert sut.validate()


@pytest.mark.parametrize(
    "lba, value",
    [(0, "0x0000000T"), (101, "0x00000002")]
)
def test_validate_실패(ssd_file_manager, command_buffer, lba, value):
    sut = WriteCommandAction(ssd_file_manager, command_buffer, lba, value)
    assert not sut.validate()
