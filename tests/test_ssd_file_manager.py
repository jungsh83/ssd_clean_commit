import os
import pytest
from src.ssd_file_manager import SSDFileManager

NAND_PATH = SSDFileManager.NAND_PATH
OUTPUT_PATH = SSDFileManager.OUTPUT_PATH
SSD_PY = os.path.join(SSDFileManager.BASE_DIR, 'src', 'ssd.py')


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
    SSDFileManager._reset_instance()
    # 파일도 삭제
    for path in [SSDFileManager.NAND_PATH, SSDFileManager.OUTPUT_PATH]:
        if os.path.exists(path):
            os.remove(path)
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
    with open(OUTPUT_PATH, encoding='utf-8') as f:
        content = f.read()
    assert content == ''


def test_write_output_정상동작_파일생성_및_내용확인(ssd_file_manager):
    test_value = "0xDEADBEEF"

    ssd_file_manager.write_output(test_value)

    assert os.path.exists(OUTPUT_PATH)
    with open(OUTPUT_PATH, encoding='utf-8') as f:
        content = f.read().strip()
    assert content == test_value

def test_lba_valid_확인(ssd_file_manager):
    test_lba = -1

    assert not ssd_file_manager._is_valid_lba(test_lba)
