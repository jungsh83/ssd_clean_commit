import pytest
from pathlib import Path
from pytest_mock import MockerFixture

from src.ssd_driver import SSDDriver, ReadException, WriteException, EraseException

DEFAULT_VALUE = '0x00000000'

data_dict = {}


def mk_read(lba):
    if not (0 <= int(lba) < 100):
        return "ERROR"
    else:
        return data_dict.get(int(lba), DEFAULT_VALUE)


def mk_write(lba, value):
    if not (0 <= int(lba) < 100):
        return "ERROR"
    else:
        data_dict[int(lba)] = value


def mk_erase(lba, size):
    # Check lba range
    for i in range(int(lba), int(lba) + int(size)):
        if not (0 <= i < 100):
            return "ERROR"

    for i in range(int(lba), int(lba) + int(size)):
        data_dict[i] = DEFAULT_VALUE

    return ""


def get_external_output(except_class, action_token, *args):
    match action_token:
        case SSDDriver.READ_TOKEN:
            return mk_read(*args)
        case SSDDriver.WRITE_TOKEN:
            return mk_write(*args)
        case SSDDriver.ERASE_TOKEN:
            return mk_erase(*args)
        case _:
            raise Exception("Unknown action token")


@pytest.fixture
def ssd_driver(mocker: MockerFixture):
    # initialize
    (Path(__file__).parent.parent / "data/ssd_nand.txt").unlink(missing_ok=True)
    (Path(__file__).parent.parent / "data/ssd_output.txt").unlink(missing_ok=True)

    mock_method = mocker.patch("src.ssd_driver.SSDDriver.get_external_output")
    mock_method.side_effect = get_external_output

    ssd_driver = SSDDriver()
    return ssd_driver


def test_read_성공(ssd_driver: SSDDriver):
    assert ssd_driver.read(0) == DEFAULT_VALUE


def test_read_실패_LBA범위초과(ssd_driver: SSDDriver):
    with pytest.raises(ReadException):
        ssd_driver.read(101)


def test_write_성공_후_데이터검증(ssd_driver: SSDDriver):
    ssd_driver.write(0, '0x00000001')
    assert ssd_driver.read(0) == '0x00000001'


def test_write_실패_LBA범위초과(ssd_driver: SSDDriver):
    with pytest.raises(WriteException):
        ssd_driver.write(101, '0x00000001')


def test_erase_성공(ssd_driver: SSDDriver):
    ssd_driver.write(0, '0x00000001')
    assert ssd_driver.read(0) == '0x00000001'

    ssd_driver.erase(0, 1)
    assert ssd_driver.read(0) == DEFAULT_VALUE


def test_erase_실패(ssd_driver: SSDDriver):
    ssd_driver.write(0, '0x00000001')
    assert ssd_driver.read(0) == '0x00000001'

    # with pytest.raises(EraseException):
    #     ssd_driver.erase(101, 1)

    with pytest.raises(EraseException):
        ssd_driver.erase(95, 10)
