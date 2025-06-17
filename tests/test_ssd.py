import pytest
from src.ssd import VirtualSSD

# data/ssd_nand.txt를 그대로 사용
NAND_FILE = "./data/ssd_nand.txt"
# 출력 파일 경로는 필요하지만, 내용 검사는 하지 않음
OUT_FILE = "./data/ssd_output.txt"

# 1) 정상 LBA를 읽는 경우
def test_정상_LBA_0_를_읽는_경우():
    ssd = VirtualSSD(NAND_FILE, OUT_FILE)
    # read(0) 은 항상 "0x00000000" 을 반환해야 함
    assert ssd.read(0) == "0x00000000"

def test_정상_LBA_0을_읽고_파일에_출력():
    """
    read() 호출 후
    data/ssd_output.txt에 한 줄로 "0x00000000"이 기록되어야 한다.
    """
    ssd = VirtualSSD(NAND_FILE, OUT_FILE)
    _ = ssd.read(0)

    with open(OUT_FILE, "r") as f:
        assert f.read().strip() == "0x00000000"

def test_정상파일_여러값을읽은후_파일에_출력():
    ssd = VirtualSSD(NAND_FILE, OUT_FILE)
    _ = ssd.read(0)  # 첫 번째 읽기 (0번 칸 → "0x00000000")
    _ = ssd.read(1)  # 두 번째 읽기 (1번 칸 → "0x00000000")

    with open(OUT_FILE, "r") as f:
        # 마지막으로 읽은 1번 칸의 값만 덮어써져 있어야 한다
        assert f.read().strip() == "0x00000000"
# 2) 기록이 없던 LBA를 읽는 경우
def test_기록이_없던_LBA를_읽는_경우():
    """
    NAND 파일에 미리 기록된 값이 없던 LBA(예: 5)를 읽으면
    항상 기본값 “0x00000000”을 반환해야 한다.
    """
    ssd = VirtualSSD(NAND_FILE, OUT_FILE)
    assert ssd.read(5) == "0x00000000"

# 3) 잘못된 LBA 범위(0~99 벗어남)
def test_잘못된_LBA_범위_0_99_벗어남():
    ssd = VirtualSSD(NAND_FILE, OUT_FILE)
    assert ssd.read(150) == "ERROR"

    with open(OUT_FILE, "r") as f:
        assert f.read().strip() == "ERROR"




def test_write_then_read_round_trip():
    """write 후 같은 LBA를 read하면 값이 같아야 한다."""
    ssd = VirtualSSD()
    ssd.write(10, "0x12345678")
    assert ssd.write(10,"0x12345678") == "0x12345678"