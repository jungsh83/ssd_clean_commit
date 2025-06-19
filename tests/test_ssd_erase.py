import pytest


@pytest.mark.parametrize("lba, size, expected_erase_start, expected_erase_end", [
    (98, 2, 98, 99),
    (5, 1, 5, 5),
    (5, 10, 5, 14),
])
def test_erase_성공(lba, size, expected_erase_start, expected_erase_end):
    ...


@pytest.mark.parametrize("lba, size", [
    (50, -100),
    (85, 100),
    (100, 10),
    (-1, 10),
    ("가나다", 10),
    (5, "가다")
])
def test_erase_파라미터_유효성오류(lba, size):
    ...
