import sys
import pytest
from io import StringIO
from pytest_mock import MockerFixture

from src.full_write_and_read_compare import FullWriteAndReadCompare


def catch_run_stdout(sut):
    stdout = sys.stdout
    output = StringIO()
    sys.stdout = output

    try:
        sut.run()

    finally:
        sys.stdout = stdout

    return output.getvalue()

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
    sut = FullWriteAndReadCompare(ssd_driver)

    # act
    out = catch_run_stdout(sut)

    # assert
    assert out == "PASS\n"

def test_수행_성공시_read_write_횟수_확인(mocker: MockerFixture):

    data_dict = {}

    def read(addr):
        return data_dict.get(addr, "0x00000000")

    def write(addr, value):
        data_dict[addr] = value

    # arrange
    ssd_driver = mocker.Mock()
    ssd_driver.read.side_effect = read
    ssd_driver.write.side_effect = write
    sut = FullWriteAndReadCompare(ssd_driver)

    # act
    out = catch_run_stdout(sut)

    # assert
    assert ssd_driver.read.call_count == 100
    assert ssd_driver.write.call_count == 100

def test_수행_실패(mocker: MockerFixture):
    data_dict = {}

    def read(addr):
        return data_dict.get(addr, "0x00000000")

    def write(addr, value):
        if addr == 33: return
        data_dict[addr] = value

    # arrange
    ssd_driver = mocker.Mock()
    ssd_driver.read.side_effect = read
    ssd_driver.write.side_effect = write
    sut = FullWriteAndReadCompare(ssd_driver)

    # act
    out = catch_run_stdout(sut)

    # assert
    assert out == "FAIL\n"



