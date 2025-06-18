import pytest
from pytest_mock import MockerFixture

from src.full_write_and_read_compare import FullWriteAndReadCompare


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


def test_수행_성공(ssd_driver):
    sut = FullWriteAndReadCompare(ssd_driver)

    # act & assert
    assert sut.run() == "PASS"


def test_수행_성공시_read_write_횟수_확인(ssd_driver):
    # arrange
    sut = FullWriteAndReadCompare(ssd_driver)

    # act
    sut.run()

    # assert
    assert ssd_driver.read.call_count == 100
    assert ssd_driver.write.call_count == 100


def test_수행_성공시_테스트_케이스_검증(ssd_driver):
    # arrange
    sut = FullWriteAndReadCompare(ssd_driver)

    # act
    sut.run()

    # assert
    samples = set(
        ssd_driver.read(i)
        for i in (0, 4, 8, 12)
    )
    assert len(samples) == 4


def test_수행_실패(ssd_driver):
    # arrange
    ssd_driver.write.side_effect = mk_write_fail
    sut = FullWriteAndReadCompare(ssd_driver)

    # act & assert
    assert sut.run() == "FAIL"


def test_수행_실패시_read_write_횟수_확인(ssd_driver):
    # arrange
    ssd_driver.write.side_effect = mk_write_fail
    sut = FullWriteAndReadCompare(ssd_driver)

    # act
    sut.run()

    # assert
    assert ssd_driver.write.call_count == 34
    assert ssd_driver.read.call_count == 34
