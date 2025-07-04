import pytest
from pytest_mock import MockFixture

from src.command_buffer.command_buffer_data import CommandBufferData, ERASE
from src.command_buffer.command_buffer_handler import CommandBufferHandler
from src.data_dict import DEFAULT_VAL
from src.ssd_commands.ssd_erase import EraseSSDCommand
from src.ssd_file_manager import SSDFileManager

COMMAND_BUFFER_HANDLER_CLASS = "src.command_buffer.command_buffer_handler.CommandBufferHandler"


@pytest.fixture
def ssd_file_manager():
    return SSDFileManager()


@pytest.fixture
def command_buffer_without_flush(mocker: MockFixture):
    mocker.patch(f"{COMMAND_BUFFER_HANDLER_CLASS}.read_all").side_effect = mk_read_all
    mocker.patch(f"{COMMAND_BUFFER_HANDLER_CLASS}.append").return_value = None
    mocker.patch(f"{COMMAND_BUFFER_HANDLER_CLASS}.is_buffer_available").return_value = True

    obj = CommandBufferHandler()
    return obj


@pytest.fixture
def command_buffer_with_flush(mocker: MockFixture):
    mocker.patch(f"{COMMAND_BUFFER_HANDLER_CLASS}.read_all").side_effect = mk_read_all
    mocker.patch(f"{COMMAND_BUFFER_HANDLER_CLASS}.append").return_value = None
    mocker.patch(f"{COMMAND_BUFFER_HANDLER_CLASS}.is_buffer_available").return_value = False

    obj = CommandBufferHandler()
    return obj


def mk_read_all():
    return [
        CommandBufferData(order=1, command_type=ERASE, lba=0, size=10),
        CommandBufferData(order=1, command_type=ERASE, lba=10, size=10),
        CommandBufferData(order=1, command_type=ERASE, lba=20, size=10),
        CommandBufferData(order=1, command_type=ERASE, lba=30, size=10),
        CommandBufferData(order=1, command_type=ERASE, lba=40, size=10),
    ]


@pytest.mark.parametrize(
    "lba, size",
    [("0", "10"), ("10", "10")]
)
def test_validate_성공(ssd_file_manager, command_buffer_without_flush, lba, size):
    assert EraseSSDCommand(ssd_file_manager, command_buffer_without_flush, lba, size).validate()


@pytest.mark.parametrize(
    "lba, size",
    [("0", "20"), ("100", "10")]
)
def test_validate_실패(mocker: MockFixture, ssd_file_manager, command_buffer_without_flush, lba, size):
    assert not EraseSSDCommand(ssd_file_manager, command_buffer_without_flush, lba, size).validate()


@pytest.mark.parametrize(
    "lba, size",
    [("0", "20"), ("100", "10")]
)
def test_run_실패(ssd_file_manager, command_buffer_without_flush, lba, size):
    assert EraseSSDCommand(ssd_file_manager, command_buffer_without_flush, lba, size).execute() == "FAIL"


@pytest.mark.parametrize(
    "lba, size, error_param",
    [("0", "20", "0"), ("100", "10", "x")]
)
def test_run_param_오류(ssd_file_manager, command_buffer_without_flush, lba, size, error_param):
    assert not EraseSSDCommand(ssd_file_manager, command_buffer_without_flush, lba, size, error_param).validate()


@pytest.mark.parametrize(
    "lba, size",
    [("0", "10"), ("10", "10"), ("0", "0")]
)
def test_run_성공_without_flush(ssd_file_manager, command_buffer_without_flush, lba, size):
    assert EraseSSDCommand(ssd_file_manager, command_buffer_without_flush, lba, size).execute() == "PASS"


@pytest.mark.parametrize(
    "lba, size",
    [("0", "10"), ("10", "10")]
)
def test_run_성공_with_flush(ssd_file_manager, command_buffer_with_flush, lba, size):
    sut = EraseSSDCommand(ssd_file_manager, CommandBufferHandler(), lba, size)
    assert sut.execute() == "PASS"

    expected_start_lba = int(lba)
    expected_end_lba = expected_start_lba + int(size) - 1

    data = sut._ssd_file_manager._load_nand()

    for i in range(expected_start_lba, expected_end_lba + 1):
        assert data[i] == DEFAULT_VAL
