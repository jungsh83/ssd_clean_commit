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

    validate_ret = erase_range_cmd.validate()
    start_lba, end_lba = erase_range_cmd._get_lba_range()

    assert validate_ret
    assert (start_lba, end_lba) == (expected_erase_start, expected_erase_end)


@pytest.mark.parametrize("start_lba, end_lba, expected_size", [
    ('5', '10', 6),
    ('10', '5', 6),
    ('0', '99', 100),
    ('99', '0', 100),
])
def test_erase_range_size_확인(start_lba, end_lba, expected_size, mock_ssd_driver):
    erase_range_cmd = EraseRangeCommand(mock_ssd_driver, start_lba, end_lba)

    validate_ret = erase_range_cmd.validate()
    start_lba, end_lba = erase_range_cmd._get_lba_range()
    size = erase_range_cmd._get_size(start_lba, end_lba)

    assert validate_ret
    assert size == expected_size


@pytest.mark.parametrize("start_lba, end_lba", [
    ('100', '1'),
    ('-1', '10'),
    ('가나다', '10'),
    ('5', '가다')
])
def test_erase_range_파라미터_유효성오류(start_lba, end_lba, mock_ssd_driver):
    erase_range_cmd = EraseRangeCommand(mock_ssd_driver, start_lba, end_lba)

    assert not erase_range_cmd.validate()
