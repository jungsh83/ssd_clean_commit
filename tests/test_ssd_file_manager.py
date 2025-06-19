import os
import pytest
from src.ssd_file_manager import SSDFileManager
import subprocess
import sys

# ───────── 경로 상수 (클래스와 동일) ─────────────────────────────────
NAND_PATH = SSDFileManager.NAND_PATH
OUTPUT_PATH = SSDFileManager.OUTPUT_PATH
SSD_PY = os.path.join(SSDFileManager.BASE_DIR, 'src', 'ssd_file_manager.py')


# ───────── 픽스처: 테스트 전후 파일 정리 ────────────────────────────
@pytest.fixture(autouse=True)
def clean_files():
    for path in (NAND_PATH, OUTPUT_PATH):
        if os.path.exists(path):
            os.remove(path)
    yield
    for path in (NAND_PATH, OUTPUT_PATH):
        if os.path.exists(path):
            os.remove(path)


@pytest.fixture
def ssd_file_manager():
    return SSDFileManager()


# 1) 정상 LBA를 읽는 경우
def test_정상_LBA_0_를_읽는_경우(ssd_file_manager):
    assert ssd_file_manager.read(0) == "0x00000000"


def test_정상_LBA_0을_읽고_파일에_출력(ssd_file_manager):
    ssd_file_manager.read(0)
    with open(OUTPUT_PATH) as f:
        assert f.read().strip() == "0x00000000"


def test_정상파일_여러값을읽은후_파일에_출력(ssd_file_manager):
    ssd_file_manager.read(0)
    ssd_file_manager.read(1)
    with open(OUTPUT_PATH) as f:
        assert f.read().strip() == "0x00000000"


# 2) 기록이 없던 LBA를 읽는 경우
def test_기록이_없던_LBA를_읽는_경우(ssd_file_manager):
    assert ssd_file_manager.read(5) == "0x00000000"


# 3) 잘못된 LBA 범위(0~99 벗어남)
def test_잘못된_LBA_범위_0_99_벗어남(ssd_file_manager):
    assert ssd_file_manager.read(150) == "ERROR"
    with open(OUTPUT_PATH) as f:
        assert f.read().strip() == "ERROR"


# ───────── write() 관련 테스트 ───────────────────────────────────────
def test_write하면_ssd_nand_txt에_해당값이_바뀐다(ssd_file_manager):
    ssd_file_manager.write(2, "0xAABBCCDD")

    with open(NAND_PATH) as f:
        lines = [line.strip() for line in f.readlines()]

    assert len(lines) == 100
    assert lines[2] == "0xAABBCCDD"
    assert all(line == "0x00000000" for i, line in enumerate(lines) if i != 2)


def test_write_여러개_하면_nand_값이_바뀐다(ssd_file_manager):
    ssd_file_manager.write(0, "0x11111111")
    ssd_file_manager.write(4, "0x12345678")
    ssd_file_manager.write(99, "0x99999999")

    with open(NAND_PATH) as f:
        lines = [line.strip() for line in f.readlines()]

    assert lines[0] == "0x11111111"
    assert lines[4] == "0x12345678"
    assert lines[99] == "0x99999999"


def test_write_lba가_invalid_값이면_output에_ERROR(ssd_file_manager):
    ssd_file_manager.write(-1, "0x12345678")

    with open(OUTPUT_PATH) as f:
        assert f.read().strip() == "ERROR"


def test_write_lba가_overflow_값이면_output에_ERROR(ssd_file_manager):
    ssd_file_manager.write(100, "0x12345678")  # 0~99만 유효

    with open(OUTPUT_PATH) as f:
        assert f.read().strip() == "ERROR"


def test_write_nand_txt_파일이_없으면_새로_파일_만든다():
    if os.path.exists(NAND_PATH):
        os.remove(NAND_PATH)

    ssd = SSDFileManager()
    ssd.write(5, "0xCAFEBABE")

    assert os.path.exists(NAND_PATH)

    with open(NAND_PATH) as f:
        lines = [line.strip() for line in f.readlines()]

    assert lines[5] == "0xCAFEBABE"


def test_쓴_값을_바로_읽어서_같은지_확인(ssd_file_manager):
    """write 후 같은 LBA를 read하면 값이 같아야 한다."""
    target_val = "0x12345678"
    ssd_file_manager.write(10, target_val)
    assert ssd_file_manager.read(10) == target_val


def test_cli에서_write하면_nand에_입력한다():
    subprocess.run([sys.executable, SSD_PY, 'W', '2', '0xDEADBEEF'], check=True)

    with open(NAND_PATH) as f:
        lines = [line.strip() for line in f.readlines()]

    assert lines[2] == '0xDEADBEEF'


def test_cli에서_read하면_nand값_읽는다(ssd_file_manager):
    ssd_file_manager.write(3, '0xABCDEF12')

    subprocess.run([sys.executable, SSD_PY, 'R', '3'], check=True)

    with open(OUTPUT_PATH) as f:
        assert f.read().strip() == '0xABCDEF12'


def test_cli에서_command가_잘못되면_output에_error입력():
    subprocess.run([sys.executable, SSD_PY, 'X', '1'], check=True)

    with open(OUTPUT_PATH) as f:
        assert f.read().strip() == 'ERROR'


def test_cli_최초실행시_output파일이_없으면_생성한다():
    if os.path.exists(OUTPUT_PATH):
        os.remove(OUTPUT_PATH)

    assert not os.path.exists(OUTPUT_PATH)

    subprocess.run([sys.executable, SSD_PY, 'R', '0'], check=True)

    assert os.path.exists(OUTPUT_PATH)

    with open(OUTPUT_PATH) as f:
        assert f.read().strip() == '0x00000000'


def test_cli_W_정상동작시_output파일은_빈파일이다():
    subprocess.run([sys.executable, SSD_PY, 'R', '100'], check=True)

    with open(OUTPUT_PATH) as f:
        assert f.read().strip() == 'ERROR'

    subprocess.run([sys.executable, SSD_PY, 'W', '10', '0xA1B2C3D4'], check=True)

    assert os.path.exists(OUTPUT_PATH)

    with open(OUTPUT_PATH, encoding='utf-8') as f:
        content = f.read()
    assert content == ''


def test_write_value가_16진수형식이_아니면_ERROR(ssd_file_manager):
    ssd_file_manager.write(5, "0xZZZZZZZZ")  # 유효하지 않은 hex 문자

    with open(OUTPUT_PATH) as f:
        assert f.read().strip() == "ERROR"


def test_cli에서_lba가_숫자가_아니면_ERROR():
    subprocess.run([sys.executable, SSD_PY, 'W', 'abc', '0x12345678'], check=True)

    with open(OUTPUT_PATH) as f:
        assert f.read().strip() == "ERROR"


def test_erase_정상작동하면해당범위가0으로바뀜(ssd_file_manager):
    ssd_file_manager.write(5, "0xA1B2C3D4")
    ssd_file_manager.write(6, "0xDEADBEEF")
    ssd_file_manager.erase(5, 2)
    lines = open(NAND_PATH).read().splitlines()
    assert lines[5] == "0x00000000"
    assert lines[6] == "0x00000000"


def test_erase_범위를벗어나면_ERROR출력(ssd_file_manager):
    ssd_file_manager.erase(95, 6)
    assert open(OUTPUT_PATH).read().strip() == "ERROR"


def test_erase_size가10초과면_ERROR출력(ssd_file_manager):
    ssd_file_manager.erase(0, 11)
    assert open(OUTPUT_PATH).read().strip() == "ERROR"


def test_erase_lba가음수면_ERROR출력(ssd_file_manager):
    ssd_file_manager.erase(-1, 2)
    assert open(OUTPUT_PATH).read().strip() == "ERROR"


def test_erase_정상작동하면_output은_빈파일이다(ssd_file_manager):
    ssd_file_manager.erase(0, 11)
    assert open(OUTPUT_PATH).read().strip() == "ERROR"
    ssd_file_manager.write(5, "0xA1B2C3D4")
    ssd_file_manager.write(6, "0xDEADBEEF")
    ssd_file_manager.erase(5, 2)
    lines = open(NAND_PATH).read().splitlines()
    assert lines[5] == "0x00000000"
    assert lines[6] == "0x00000000"

    assert os.path.exists(OUTPUT_PATH)

    with open(OUTPUT_PATH, encoding='utf-8') as f:
        content = f.read()
    assert content == ''

def test_erase_size0이면_아무것도_안지움(ssd_file_manager):
    ssd_file_manager.write(5, "0xA1B2C3D4")
    ssd_file_manager.write(6, "0xDEADBEEF")
    ssd_file_manager.erase(5, 0)
    lines = open(NAND_PATH).read().splitlines()
    assert lines[5] == "0xA1B2C3D4"
    assert lines[6] == "0xDEADBEEF"