import pytest
from pathlib import Path
from pytest_mock import MockerFixture

from src.ssd_driver import SSDDriver, ReadException, WriteException


@pytest.fixture
def ssd_driver():
    # initialize
    (Path(__file__).parent.parent / "data/ssd_nand.txt").unlink(missing_ok=True)
    (Path(__file__).parent.parent / "data/ssd_output.txt").unlink(missing_ok=True)

    ssd_driver = SSDDriver()
    return ssd_driver


def test_read_성공(ssd_driver: SSDDriver):
    assert ssd_driver.read(0) == '0x00000000'


def test_read_실패_LBA범위초과(ssd_driver: SSDDriver):
    with pytest.raises(ReadException):
        ssd_driver.read(101)


def test_write_성공_후_데이터검증(ssd_driver: SSDDriver):
    ssd_driver.write(0, '0x00000001')
    assert ssd_driver.read(0) == '0x00000001'


def test_write_실패_LBA범위초과(ssd_driver: SSDDriver):
    with pytest.raises(WriteException):
        ssd_driver.write(101, '0x00000001')
