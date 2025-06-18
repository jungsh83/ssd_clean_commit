import pytest
from pytest_mock import MockerFixture

from src.full_write_and_read_compare import FullWriteAndReadCompare


def test_수행_성공(mocker: MockerFixture):
    data_dict = {}

    def read(lba):
        return data_dict.get(lba, "0x00000000")

    def write(lba, value):
        data_dict[lba] = value

    # arrange
    ssd_driver = mocker.Mock()
    ssd_driver.read.side_effect = read
    ssd_driver.write.side_effect = write
    sut = FullWriteAndReadCompare(ssd_driver)

    # act & assert
    assert sut.run() == "PASS"


def test_수행_성공시_read_write_횟수_확인(mocker: MockerFixture):
    data_dict = {}

    def read(lba):
        return data_dict.get(lba, "0x00000000")

    def write(lba, value):
        data_dict[lba] = value

    # arrange
    ssd_driver = mocker.Mock()
    ssd_driver.read.side_effect = read
    ssd_driver.write.side_effect = write
    sut = FullWriteAndReadCompare(ssd_driver)

    # act
    sut.run()

    # assert
    assert ssd_driver.read.call_count == 100
    assert ssd_driver.write.call_count == 100


def test_수행_성공시_테스트_케이스_검증(mocker: MockerFixture):
    data_dict = {}

    def read(lba):
        return data_dict.get(lba, "0x00000000")

    def write(lba, value):
        data_dict[lba] = value

    # arrange
    ssd_driver = mocker.Mock()
    ssd_driver.read.side_effect = read
    ssd_driver.write.side_effect = write
    sut = FullWriteAndReadCompare(ssd_driver)

    # act
    sut.run()

    # assert
    samples = set(
        ssd_driver.read(i)
        for i in (0, 4, 8, 12)
    )
    assert len(samples) == 4


def test_수행_실패(mocker: MockerFixture):
    data_dict = {}

    def read(lba):
        return data_dict.get(lba, "0x00000000")

    def write(lba, value):
        if lba == 33: return
        data_dict[lba] = value

    # arrange
    ssd_driver = mocker.Mock()
    ssd_driver.read.side_effect = read
    ssd_driver.write.side_effect = write
    sut = FullWriteAndReadCompare(ssd_driver)

    # act & assert
    assert sut.run() == "FAIL"


def test_수행_실패시_read_write_횟수_확인(mocker: MockerFixture):
    data_dict = {}

    def read(lba):
        return data_dict.get(lba, "0x00000000")

    def write(lba, value):
        if lba == 49: return
        data_dict[lba] = value

    # arrange
    ssd_driver = mocker.Mock()
    ssd_driver.read.side_effect = read
    ssd_driver.write.side_effect = write
    sut = FullWriteAndReadCompare(ssd_driver)

    # act
    sut.run()

    # assert
    assert ssd_driver.write.call_count == 50
    assert ssd_driver.read.call_count == 50
