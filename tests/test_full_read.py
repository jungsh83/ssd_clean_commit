from src.full_read import FullRead
from src.ssd import VirtualSSD
import pytest

def test_fullread_100줄_출력_확인(capsys):
    ssd = VirtualSSD()
    action = FullRead(ssd)  # 인자 없는 커맨드
    action.run()

    # 3) 단언
    lines = capsys.readouterr().out.strip().splitlines()
    assert len(lines) == 100  # 100줄인지 확인

def test_fullread_first_line_matches_lba0():
    pass

def test_fullread_last_line_matches_lba99():
    pass