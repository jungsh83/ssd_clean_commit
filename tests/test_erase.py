import pytest


@pytest.mark.parametrize("lba, size, expected_erase_start, expected_erase_end", [
    (98, 10, 98, 99),
    (50, 100, 50, 99),
    (0, 999, 0, 99),
    (10, -10, 1, 10),
    (5, -2, 4, 5),
    (5, 1, 5, 5),
    (5, -1, 5, 5),
    (50, -100, 0, 50),
    (85, 100, 85, 99)
])
def test_erase_command_성공(lba, size, expected_erase_start, expected_erase_end):
    ...


@pytest.mark.parametrize("lba, size", [
    (100, 10),
    (-1, 10),
    ("가나다", 10),
    (5, "가다")
])
def test_erase_command_파라미터_유효성오류(lba, size):
    ...
