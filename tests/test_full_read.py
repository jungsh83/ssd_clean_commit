from src.full_read import FullRead
from src.ssd import VirtualSSD
import pytest

def test_fullread_100줄_출력_확인(capsys):
    ssd = VirtualSSD()
    action = FullRead(ssd)  # 인자 없는 커맨드
    action.run()

    lines = capsys.readouterr().out.strip().splitlines()
    assert len(lines) == 100  # 100줄인지 확인

def test_fullread_1줄출력이_첫번째와같은지_확인(capsys):
    ssd = VirtualSSD()
    FullRead(ssd).run()

    lines = capsys.readouterr().out.splitlines()
    assert lines[0] == ssd.read(0)

def test_fullread_100줄출력이_마지막과_같은지_화인(capsys):
    ssd = VirtualSSD()
    FullRead(ssd).run()

    lines = capsys.readouterr().out.splitlines()
    assert lines[-1] == ssd.read(VirtualSSD.LBA_COUNT - 1)

def test_fullread_매개변수_유효성검사(capsys):
    cmd = FullRead(VirtualSSD(), "dummy")   # 인자 1개
    assert not cmd.validate()               # ① 실패해야 함

    # 혹은 validate() 없어도 run() 해보면 ERROR 출력
    cmd.run()
    assert "ERROR" in capsys.readouterr().out

