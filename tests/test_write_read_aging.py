import pytest
from pytest_mock import MockerFixture

from src.write_read_aging import WriteReadAging


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
    sut = WriteReadAging(ssd_driver)

    # act
    # assert
    assert sut.run() == "PASS"


def test_수행_성공시_read_write_횟수_점검(mocker: MockerFixture):
    data_dict = {}

    def read(lba):
        return data_dict.get(lba, "0x00000000")

    def write(lba, value):
        data_dict[lba] = value

    # arrange
    ssd_driver = mocker.Mock()
    ssd_driver.read.side_effect = read
    ssd_driver.write.side_effect = write
    sut = WriteReadAging(ssd_driver)

    # act
    sut.run()

    # assert
    assert ssd_driver.write.call_count == 400
    assert ssd_driver.read.call_count == 400


def test_수행_실패(mocker: MockerFixture):
    data_dict = {}

    def read(lba):
        return data_dict.get(lba, "0x00000000")

    def write(lba, value):
        if lba == 99: return
        data_dict[lba] = value

    # arrange
    ssd_driver = mocker.Mock()
    ssd_driver.read.side_effect = read
    ssd_driver.write.side_effect = write
    sut = WriteReadAging(ssd_driver)

    # act
    # assert
    assert sut.run() == "FAIL"


def test_수행_실패시_read_write_횟수_점검(mocker: MockerFixture):
    data_dict = {}

    def read(lba):
        return data_dict.get(lba, "0x00000000")

    def write(lba, value):
        if lba == 99: return
        data_dict[lba] = value

    # arrange
    ssd_driver = mocker.Mock()
    ssd_driver.read.side_effect = read
    ssd_driver.write.side_effect = write
    sut = WriteReadAging(ssd_driver)

    # act
    sut.run()

    # assert
    assert ssd_driver.write.call_count == 2
    assert ssd_driver.read.call_count == 2
