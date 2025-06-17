import pytest
from src.ssd import VirtualSSD
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'ssd_nand.txt')
OUTPUT_PATH = os.path.join(BASE_DIR, 'data', 'ssd_output.txt')


@pytest.fixture(autouse=True)
def clean_files():
    # 테스트 전후로 파일 정리
    yield
    if os.path.exists(DATA_PATH):
        os.remove(DATA_PATH)
    if os.path.exists(OUTPUT_PATH):
        os.remove(OUTPUT_PATH)


def test_write하면_ssd_nand_txt에_해당값이_바뀐다():
    ssd = VirtualSSD()
    ssd.write(2, '0xAABBCCDD')

    with open(DATA_PATH) as f:
        lines = [line.strip() for line in f.readlines()]

    assert len(lines) == 100
    assert lines[2] == '0xAABBCCDD'
    assert all(line == '0x00000000' for i, line in enumerate(lines) if i != 2)


@pytest.mark.skip
def test_write_여러개_하면_nand_값이_바뀐다():
    ssd = VirtualSSD()
    ssd.write(0, '0x11111111')
    ssd.write(4, '0x12345678')
    ssd.write(99, '0x99999999')

    with open(DATA_PATH) as f:
        lines = [line.strip() for line in f.readlines()]

    assert lines[0] == '0x11111111'
    assert lines[4] == '0x12345678'
    assert lines[99] == '0x99999999'


@pytest.mark.skip
def test_write_invalid_값이면_output에_ERROR():
    ssd = VirtualSSD()
    ssd.write(-1, '0x12345678')

    with open(OUTPUT_PATH) as f:
        assert f.read().strip() == 'ERROR'


@pytest.mark.skip
def test_write_overflow_값이면_output에_ERROR():
    ssd = VirtualSSD()
    ssd.write(100, '0x12345678')  # 0~99까지만 유효

    with open(OUTPUT_PATH) as f:
        assert f.read().strip() == 'ERROR'


@pytest.mark.skip
def test_write_nand_txt_파일이_없으면_새로_파일_만든다():
    if os.path.exists(DATA_PATH):
        os.remove(DATA_PATH)

    ssd = VirtualSSD()
    ssd.write(5, '0xCAFEBABE')

    assert os.path.exists(DATA_PATH)

    with open(DATA_PATH) as f:
        lines = [line.strip() for line in f.readlines()]

    assert lines[5] == '0xCAFEBABE'
