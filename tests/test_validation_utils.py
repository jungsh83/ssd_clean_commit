import pytest
from src.ssd_commands import validate_lba, validate_value


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
