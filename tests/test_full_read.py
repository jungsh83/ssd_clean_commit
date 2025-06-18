# tests/test_full_read.py
import os
import pytest

from src.full_read import FullRead
from src.ssd import VirtualSSD

@pytest.fixture
def ssd(tmp_path):
    """깨끗한 VirtualSSD 인스턴스 반환."""
    for p in (VirtualSSD.NAND_PATH, VirtualSSD.OUTPUT_PATH):
        if os.path.exists(p):
            os.remove(p)
    return VirtualSSD()


def test_fullread_100줄_출력확인(ssd, capsys):
    FullRead(ssd).run()
    assert len(capsys.readouterr().out.splitlines()) == VirtualSSD.LBA_COUNT

@pytest.mark.parametrize("index", [0, VirtualSSD.LBA_COUNT - 1])
def test_fullread_lba_출력줄양끝단_검증(ssd, capsys, index):
    FullRead(ssd).run()
    lines = capsys.readouterr().out.splitlines()
    assert lines[index] == ssd.read(index)


def test_fullread_유효성범위검사(ssd, capsys):
    cmd = FullRead(ssd, "dummy")
    assert not cmd.validate()
    cmd.run()
    assert "ERROR" in capsys.readouterr().out
