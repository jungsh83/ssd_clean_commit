import pytest
from pytest_mock import MockerFixture

from src.shell_commands.script.erase_and_write_aging import EraseAndWriteAgingCommand

DEFULAT_VALUE = "0x00000000"

data_dict = {}


def mk_read(lba):
    if not (0 <= lba < 100): return "ERROR"
    return data_dict.get(lba, DEFULAT_VALUE)


def mk_read_fail(lba):
    if lba == 2: return "ERROR"
    return data_dict.get(lba, DEFULAT_VALUE)


def mk_write(lba, value):
    if not (0<=lba<100): return "ERROR"
    data_dict[lba] = value


def mk_erase(lba, size):
    for i in range(lba, lba + size):
        data_dict[i] = DEFULAT_VALUE


@pytest.fixture
def ssd_driver(mocker: MockerFixture):
    mk = mocker.Mock()
    mk.read.side_effect = mk_read
    mk.write.side_effect = mk_write
    mk.erase.side_effect = mk_erase

    return mk


@pytest.fixture
def ssd_driver_fail(mocker: MockerFixture):
    mk = mocker.Mock()
    mk.read.side_effect = mk_read_fail
    mk.write.side_effect = mk_write
    mk.erase.side_effect = mk_erase

    return mk


def test_validate_수행_성공(ssd_driver):
    # act & assert
    assert EraseAndWriteAgingCommand(ssd_driver).validate()


def test_validate_수행_실패(ssd_driver):
    # act & assert
    assert not EraseAndWriteAgingCommand(ssd_driver, 1, "0x12345678").validate()


def test_수행_성공(ssd_driver):
    assert EraseAndWriteAgingCommand(ssd_driver).execute() == "PASS"


def test_수행_성공시_read_write_erase_횟수_확인(ssd_driver):
    # act
    EraseAndWriteAgingCommand(ssd_driver).execute()

    # assert
    assert ssd_driver.erase.call_count == 1 + 30 * 48
    assert ssd_driver.write.call_count == 30 * 48 * 2
    assert ssd_driver.read.call_count == 30 * 48 * 3


def test_수행_실패(ssd_driver_fail):
    assert EraseAndWriteAgingCommand(ssd_driver_fail).execute() == "FAIL"


def test_수행_실패시_read_write_erase_횟수_확인(ssd_driver_fail):
    # act
    EraseAndWriteAgingCommand(ssd_driver_fail).execute()

    # assert
    assert ssd_driver_fail.erase.call_count == 1 + 1
    assert ssd_driver_fail.write.call_count == 2
    assert ssd_driver_fail.read.call_count == 1
