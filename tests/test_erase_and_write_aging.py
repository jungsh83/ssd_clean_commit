import pytest
from pytest_mock import MockerFixture

from src.commands.erase_and_write_aging import EraseAndWriteAging

data_dict = {}

def mk_read(lba):
    return data_dict.get(lba, "0x00000000")

def mk_read_fail(lba):
    if lba == 2: return "ERROR"
    return data_dict.get(lba, "0x00000000")

def mk_write(lba, value):
    data_dict[lba] = value

def mk_erase(lba, size):
    for i in range(lba, lba+size):
        data_dict[i] = "0x00000000"

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
    assert EraseAndWriteAging(ssd_driver).validate()


def test_validate_수행_실패(ssd_driver):
    # act & assert
    assert not EraseAndWriteAging(ssd_driver, 1, "0x12345678").validate()

def test_수행_성공(ssd_driver):
    assert EraseAndWriteAging(ssd_driver).run() == "PASS"


def test_수행_성공시_read_write_erase_횟수_확인(ssd_driver):
    # act
    EraseAndWriteAging(ssd_driver).run()

    # assert
    assert ssd_driver.erase.call_count == 1 + 30 * 33
    assert ssd_driver.write.call_count == 30 * 33 * 2
    assert ssd_driver.read.call_count == 30 * 33 * 3


def test_수행_실패(ssd_driver_fail):
    assert EraseAndWriteAging(ssd_driver_fail).run() == "FAIL"


def test_수행_실패시_read_write_erase_횟수_확인(ssd_driver_fail):
    # act
    EraseAndWriteAging(ssd_driver_fail).run()

    # assert
    assert ssd_driver_fail.erase.call_count == 1 + 1
    assert ssd_driver_fail.write.call_count == 2
    assert ssd_driver_fail.read.call_count == 1
