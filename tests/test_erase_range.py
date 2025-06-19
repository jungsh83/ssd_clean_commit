import pytest


@pytest.mark.parametrize("start_lba, end_lba, expected_erase_start, expected_erase_end", [
    (5, 10, 5, 10),
    (10, 5, 5, 10),
])
def test_erase_range_성공(start_lba, end_lba, expected_erase_start, expected_erase_end):
    ...


@pytest.mark.parametrize("start_lba, end_lba", [
    (100, 1),
    (-1, 10),
    ("가나다", 10),
    (5, "가다")
])
def test_erase_range_파라미터_유효성오류(start_lba, end_lba):
    ...
