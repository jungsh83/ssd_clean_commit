# tests/test_full_read.py
import pytest

from src.full_read import FullRead
from src.ssd import VirtualSSD


@pytest.fixture
def ssd_driver(mocker):
    driver = mocker.Mock()
    driver.LBA_COUNT = VirtualSSD.LBA_COUNT  # 100
    driver.read.side_effect = lambda lba: f"0x{lba:08X}"
    return driver


def test_fullread_100줄_출력확인(ssd_driver, capsys):
    FullRead(ssd_driver).run()
    assert len(capsys.readouterr().out.splitlines()) == VirtualSSD.LBA_COUNT


def test_fullread_첫줄_LBA0_값확인(ssd_driver, capsys):
    FullRead(ssd_driver).run()
    lines = capsys.readouterr().out.splitlines()
    assert lines[0] == "0x00000000"


def test_fullread_마지막줄_LBA99_값확인(ssd_driver, capsys):
    FullRead(ssd_driver).run()
    lines = capsys.readouterr().out.splitlines()

    expected = f"0x{VirtualSSD.LBA_COUNT - 1:08X}"  # 0x00000063
    assert lines[-1] == expected


def test_fullread_유효성범위검사(ssd_driver):
    cmd = FullRead(ssd_driver, "dummy")  # 인자 1개 → validate 실패
    assert not cmd.validate()

    with pytest.raises(ValueError) as exc:
        cmd.run()

    assert str(exc.value) == FullRead.ERROR_UNVALIDATED
