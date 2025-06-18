import os
import pytest

from src.full_read import FullRead
from src.ssd import VirtualSSD


@pytest.fixture
def ssd(tmp_path):
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


def test_fullread_유효성범위검사(ssd):
    cmd = FullRead(ssd, "dummy")          # 인자 1개 → validate 실패
    assert not cmd.validate()             # 사전 체크

    with pytest.raises(ValueError) as exc:
        cmd.run()

    assert str(exc.value) == FullRead.ERROR_UNVALIDATED
