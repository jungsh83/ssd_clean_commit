import pytest
from pytest_mock import MockerFixture

from src.shell_commands.script.write_read_aging import WriteReadAgingShellCommand

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

@pytest.fixture
def ssd_driver_fail(mocker: MockerFixture):
    mk = mocker.Mock()
    mk.read.side_effect = mk_read
    mk.write.side_effect = mk_write_fail

    return mk


def test_validate_수행_성공(ssd_driver):
    # act & assert
    assert WriteReadAgingShellCommand(ssd_driver).validate()


def test_validate_수행_실패(ssd_driver):
    # act & assert
    assert not WriteReadAgingShellCommand(ssd_driver, 1, "0x12345678").validate()


def test_수행_성공(ssd_driver):
    # act & assert
    assert WriteReadAgingShellCommand(ssd_driver).execute() == "PASS"


def test_수행_성공시_read_write_횟수_점검(ssd_driver):
    # act
    WriteReadAgingShellCommand(ssd_driver).execute()

    # assert
    assert ssd_driver.write.call_count == 400
    assert ssd_driver.read.call_count == 400


def test_수행_실패(ssd_driver_fail):
    assert WriteReadAgingShellCommand(ssd_driver_fail).execute() == "FAIL"


def test_수행_실패시_read_write_횟수_점검(ssd_driver_fail):
    # act
    WriteReadAgingShellCommand(ssd_driver_fail).execute()

    # assert
    assert ssd_driver_fail.write.call_count == 201
    assert ssd_driver_fail.read.call_count == 201
