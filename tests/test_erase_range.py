import pytest

from src.commands.erase_range import EraseRangeCommand
from src.ssd_driver import SSDDriver


@pytest.fixture
def mock_ssd_driver(mocker):
    return mocker.Mock(spec=SSDDriver)


@pytest.mark.parametrize("start_lba, end_lba, expected_erase_start, expected_erase_end", [
    ('5', '10', 5, 10),
    ('10', '5', 5, 10),
])
def test_erase_range_체크(start_lba, end_lba, expected_erase_start, expected_erase_end, mock_ssd_driver):
    erase_range_cmd = EraseRangeCommand(mock_ssd_driver, start_lba, end_lba)

    start_lba, end_lba = erase_range_cmd._get_lba_range()

    assert (start_lba, end_lba) == (expected_erase_start, expected_erase_end)


@pytest.mark.parametrize("start_lba, end_lba", [
    ('100', '1'),
    ('-1', '10'),
    ('가나다', '10'),
    ('5', '가다')
])
def test_erase_range_파라미터_유효성오류(start_lba, end_lba):
    ...
