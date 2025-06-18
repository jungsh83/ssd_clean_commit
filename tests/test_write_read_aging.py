import pytest
from pytest_mock import MockerFixture

from src.write_read_aging import WriteReadAging


def test_수행_성공(mocker: MockerFixture):
    data_dict = {}

    def read(addr):
        return data_dict.get(addr, "0x00000000")

    def write(addr, value):
        data_dict[addr] = value

    # arrange
    ssd_driver = mocker.Mock()
    ssd_driver.read.side_effect = read
    ssd_driver.write.side_effect = write
    sut = WriteReadAging(ssd_driver)

    # act
    out = sut.run()

    # assert
    assert out == "PASS"


def test_수행_성공시_read_write_횟수_점검(mocker: MockerFixture):
    data_dict = {}

    def read(addr):
        return data_dict.get(addr, "0x00000000")

    def write(addr, value):
        data_dict[addr] = value

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

    def read(addr):
        return data_dict.get(addr, "0x00000000")

    def write(addr, value):
        if addr == 99: return
        data_dict[addr] = value

    # arrange
    ssd_driver = mocker.Mock()
    ssd_driver.read.side_effect = read
    ssd_driver.write.side_effect = write
    sut = WriteReadAging(ssd_driver)

    # act
    out = sut.run()

    # assert
    assert out == "FAIL"


def test_수행_실패시_read_write_횟수_점검(mocker: MockerFixture):
    data_dict = {}

    def read(addr):
        return data_dict.get(addr, "0x00000000")

    def write(addr, value):
        if addr == 99: return
        data_dict[addr] = value

    # arrange
    ssd_driver = mocker.Mock()
    ssd_driver.read.side_effect = read
    ssd_driver.write.side_effect = write
    sut = WriteReadAging(ssd_driver)

    # act
    out = sut.run()

    # assert
    assert ssd_driver.write.call_count == 2
    assert ssd_driver.read.call_count == 2
