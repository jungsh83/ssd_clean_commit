import pytest
from pytest_mock import MockerFixture

from src.commands.full_write_and_read_compare import FullWriteAndReadCompareCommand
from src.ssd import VirtualSSD

data_dict = {}

def mk_read(lba):
    return data_dict.get(lba, "0x00000000")

def mk_write(lba, value):
    data_dict[lba] = value

def mk_write_fail(lba, value):
    if lba == 33: return
    data_dict[lba] = value

@pytest.fixture
def ssd_driver(mocker: MockerFixture):
    mk = mocker.Mock()
    mk.read.side_effect = mk_read
    mk.write.side_effect = mk_write

    return mk

@pytest.fixture
def ssd_driver_fail(mocker: MockerFixture):
    mk = mocker.Mock()
    mk.read.side_effect = mk_read
    mk.write.side_effect = mk_write_fail

    return mk

def test_validate_수행_성공(ssd_driver):
    # act & assert
    assert FullWriteAndReadCompareCommand(ssd_driver).validate()


def test_validate_수행_실패(ssd_driver):
    # act & assert
    assert not FullWriteAndReadCompareCommand(ssd_driver, 1, "0x12345678").validate()

def test_수행_성공(ssd_driver):
    assert FullWriteAndReadCompareCommand(ssd_driver).run() == "PASS"


def test_수행_성공시_read_write_횟수_확인(ssd_driver):
    # act
    FullWriteAndReadCompareCommand(ssd_driver).run()

    # assert
    assert ssd_driver.read.call_count == VirtualSSD.LBA_COUNT
    assert ssd_driver.write.call_count == VirtualSSD.LBA_COUNT


def test_수행_성공시_테스트_케이스_검증(ssd_driver):
    # act
    FullWriteAndReadCompareCommand(ssd_driver).run()

    # assert
    samples = set(
        ssd_driver.read(i)
        for i in (0, 4, 8, 12)
    )
    assert len(samples) == 4


def test_수행_실패(ssd_driver_fail):
    assert FullWriteAndReadCompareCommand(ssd_driver_fail).run() == "FAIL"


def test_수행_실패시_read_write_횟수_확인(ssd_driver_fail):
    # act
    FullWriteAndReadCompareCommand(ssd_driver_fail).run()

    # assert
    assert ssd_driver_fail.write.call_count == 34
    assert ssd_driver_fail.read.call_count == 34
