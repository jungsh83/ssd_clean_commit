import pytest
from src.ssd import VirtualSSD
from pathlib import Path

NAND_PATH = Path(__file__).parent.parent / "data" / "ssd_nand.txt"


# 1) 정상 LBA를 읽는 경우
def test_read_valid_lba(tmp_path):
    pass
def test_read_valid_lba_should_return_value_and_write_to_output(tmp_path):
    pass

# 2) 기록이 없던 LBA를 읽는 경우
def test_read_unwritten_lba_returns_zero_and_writes_zero(tmp_path):
    pass

# 3) 잘못된 LBA 범위(0~99 벗어남)
def test_read_invalid_lba_writes_error(tmp_path):
    pass




def test_write_then_read_round_trip():
    """write 후 같은 LBA를 read하면 값이 같아야 한다."""
    ssd = VirtualSSD()
    ssd.write(10, "0x12345678")
    assert ssd.write(10,"0x12345678") == "0x12345678"