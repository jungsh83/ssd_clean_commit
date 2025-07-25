import pytest
from pytest_mock import MockFixture

from src.ssd_file_manager import SSDFileManager
from src.command_buffer.command_buffer_handler import CommandBufferHandler
from src.command_buffer.command_buffer_data import CommandBufferData, WRITE
from src.ssd_commands.ssd_write import WriteSSDCommand

COMMAND_BUFFER_HANDLER_CLASS = "src.command_buffer.command_buffer_handler.CommandBufferHandler"


@pytest.fixture
def ssd_file_manager():
    return SSDFileManager()


@pytest.fixture
def command_buffer(mocker: MockFixture):
    mocker.patch(f"{COMMAND_BUFFER_HANDLER_CLASS}.read_all").side_effect = mk_read_all
    mocker.patch(f"{COMMAND_BUFFER_HANDLER_CLASS}.append").return_value = None
    mocker.patch(f"{COMMAND_BUFFER_HANDLER_CLASS}.is_buffer_available").return_value = True

    obj = CommandBufferHandler()
    return obj


def mk_read_all():
    return [
        CommandBufferData(order=1, command_type=WRITE, lba=0, value="0x00000000"),
        CommandBufferData(order=1, command_type=WRITE, lba=1, value="0x00000001"),
        CommandBufferData(order=1, command_type=WRITE, lba=2, value="0x00000002"),
        CommandBufferData(order=1, command_type=WRITE, lba=3, value="0x00000003"),
        CommandBufferData(order=1, command_type=WRITE, lba=4, value="0x00000004"),
    ]


@pytest.mark.parametrize(
    "lba, value",
    [("0", "0x00000001"), ("33", "0x00000002")]
)
def test_validate_성공(ssd_file_manager, command_buffer, lba, value):
    assert WriteSSDCommand(ssd_file_manager, command_buffer, lba, value).validate()


def test_validate_실패_no_arguments(mocker: MockFixture, ssd_file_manager, command_buffer):
    "src.ssd_commands.(validate_lba, validate_value) 구성 후 Test"
    assert not WriteSSDCommand(ssd_file_manager, command_buffer).validate()


@pytest.mark.parametrize(
    "lba, value",
    [("-5", "0x0000000T"), ("0", "0x0000000T"), ("101", "0x00000002")]
)
def test_validate_실패(mocker: MockFixture, ssd_file_manager, command_buffer, lba, value):
    assert not WriteSSDCommand(ssd_file_manager, command_buffer, lba, value).validate()


@pytest.mark.parametrize(
    "lba, value",
    [("0", "0x0000000T"), ("101", "0x00000002")]
)
def test_run_실패(ssd_file_manager, command_buffer, lba, value):
    assert WriteSSDCommand(ssd_file_manager, command_buffer, lba, value).execute() == "FAIL"


@pytest.mark.parametrize(
    "lba, value",
    [("0", "0x00000001"), ("99", "0x00000099")]
)
def test_run_성공_without_flush(ssd_file_manager, command_buffer, lba, value):
    assert WriteSSDCommand(ssd_file_manager, command_buffer, lba, value).execute() == "PASS"


@pytest.mark.parametrize(
    "lba, value",
    [("0", "0x00000001"), ("99", "0x00000099")]
)
def test_run_성공_with_flush(mocker: MockFixture, ssd_file_manager, command_buffer, lba, value):
    mocker.patch(f"{COMMAND_BUFFER_HANDLER_CLASS}.is_buffer_available").return_value = False
    assert WriteSSDCommand(ssd_file_manager, command_buffer, lba, value).execute() == "PASS"
