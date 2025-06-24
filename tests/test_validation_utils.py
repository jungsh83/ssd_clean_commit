import pytest
from src.ssd_commands import validate_lba, validate_value, validate_erase_size
from src.data_dict import ERASE_SIZE_MIN, ERASE_SIZE_MAX


@pytest.mark.parametrize("input_lba, expected", [
    ("0", True),
    ("99", True),
    ("100", False),
    ("-1", False),
    ("abc", False),
    ("", False),
])
def test_validate_lba_경계값_및_형식검증(input_lba, expected):
    assert validate_lba(input_lba) == expected


@pytest.mark.parametrize("input_val, expected", [
    ("0x12345678", True),
    ("0xABCDEF12", True),
    ("0xabcdef12", False),
    ("0x1234", False),
    ("0x1234567890", False),
    ("12345678", False),
    ("0x1234567G", False),
    ("0x1234Z678", False),
    ("", False),
])
def test_validate_value_다양한_형식_검증(input_val, expected):
    assert validate_value(input_val) == expected


def test_유효한_erase_size_범위():
    for i in range(ERASE_SIZE_MIN, ERASE_SIZE_MAX + 1):
        assert validate_erase_size("0", str(i)) is True


def test_erase_size가_숫자가_아니면_false():
    assert validate_erase_size("0", "abc") is False
    assert validate_erase_size("0", "5.5") is False
    assert validate_erase_size("0", "-1") is False
    assert validate_erase_size("0", "") is False


def test_erase_size가_범위를_벗어나면_false():
    assert validate_erase_size("0", str(ERASE_SIZE_MIN - 1)) is False
    assert validate_erase_size("0", str(ERASE_SIZE_MAX + 1)) is False
    assert validate_erase_size("95", "6") is False


@pytest.mark.parametrize("lba,size", [
    ("90", "11"),
    ("95", "10"),
    ("100", "1"),
])
def test_validate_erase_size_LBA_초과(lba, size):
    assert validate_erase_size(lba, size) is False
