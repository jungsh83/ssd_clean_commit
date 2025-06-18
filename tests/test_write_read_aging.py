import pytest
from pytest_mock import MockerFixture

from src.write_read_aging import WriteReadAging


data_dict = {}

def mk_read(lba):
    return data_dict.get(lba, "0x00000000")

def mk_write(lba, value):
    data_dict[lba] = value

def mk_write_fail(lba, value):
    if lba == 99: return
    data_dict[lba] = value

@pytest.fixture
def ssd_driver(mocker: MockerFixture):
    mk = mocker.Mock()
    mk.read.side_effect = mk_read
    mk.write.side_effect = mk_write

    return mk


def test_수행_성공(ssd_driver):
    # act & assert
    assert WriteReadAging(ssd_driver).run() == "PASS"


def test_수행_성공시_read_write_횟수_점검(ssd_driver):
    # act
    WriteReadAging(ssd_driver).run()

    # assert
    assert ssd_driver.write.call_count == 400
    assert ssd_driver.read.call_count == 400


def test_수행_실패(ssd_driver):
    ssd_driver.write.side_effect = mk_write_fail

    # act & assert
    assert WriteReadAging(ssd_driver).run() == "FAIL"


def test_수행_실패시_read_write_횟수_점검(ssd_driver):
    ssd_driver.write.side_effect = mk_write_fail

    # act
    WriteReadAging(ssd_driver).run()

    # assert
    assert ssd_driver.write.call_count == 201
    assert ssd_driver.read.call_count == 201
