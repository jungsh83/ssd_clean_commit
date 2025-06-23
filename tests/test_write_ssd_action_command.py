import pytest
from pytest_mock import MockFixture

from src.command_buffer.command_buffer_data import CommandBufferData
from src.command_buffer.command_buffer_handler import CommandBufferHandler
from src.ssd_file_manager import SSDFileManager
from src.ssd_commands.ssd_write import WriteCommandAction


@pytest.fixture
def ssd_file_manager():
    return SSDFileManager()


@pytest.fixture
def command_buffer(mocker: MockFixture):
    mock_method = mocker.patch("src.command_buffer.command_buffer_handler.CommandBufferHandler.read_all")
    mock_method.side_effect = mk_read_all

    obj = CommandBufferHandler()
    return obj


def mk_read_all():
    return [
        CommandBufferData(order=1, command_type="W", lba=0, value="0x00000000"),
        CommandBufferData(order=1, command_type="W", lba=1, value="0x00000001"),
        CommandBufferData(order=1, command_type="W", lba=2, value="0x00000002"),
        CommandBufferData(order=1, command_type="W", lba=3, value="0x00000003"),
        CommandBufferData(order=1, command_type="W", lba=4, value="0x00000004"),
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
