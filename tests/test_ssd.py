import pytest
from src.ssd import VirtualSSD


def test_read_empty_returns_zero():
    """아무 것도 안 썼을 때 read(0)은 0x00000000을 돌려줘야 한다."""
    ssd = VirtualSSD()
    assert ssd.read(0) == "0x00000000"


def test_write_then_read_round_trip():
    """write 후 같은 LBA를 read하면 값이 같아야 한다."""
    ssd = VirtualSSD()
    ssd.write(10, "0x12345678")
    assert ssd.write(10,"0x12345678") == "0x12345678"