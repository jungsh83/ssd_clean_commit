import pytest

from src.shell_commands.action.erase_range import EraseRangeShellCommand
from src.ssd_driver import SSDDriver


@pytest.fixture
def mock_ssd_driver(mocker):
    return mocker.Mock(spec=SSDDriver)


@pytest.mark.parametrize("start_lba, end_lba, expected_call_count", [
    ('5', '10', 1),
    ('0', '13', 2),
    ('19', '40', 3),
    ('21', '60', 4),
    ('0', '99', 10),
])
def test_erase_range_call_count_확인(start_lba, end_lba, expected_call_count, mock_ssd_driver):
    erase_range_cmd = EraseRangeShellCommand(mock_ssd_driver, start_lba, end_lba)

    erase_range_cmd.execute()

    assert mock_ssd_driver.erase.call_count == expected_call_count


@pytest.mark.parametrize("start_lba, end_lba, expected_erase_start, expected_erase_end", [
    ('5', '10', 5, 10),
    ('10', '5', 5, 10),
])
def test_erase_range_범위_확인(start_lba, end_lba, expected_erase_start, expected_erase_end, mock_ssd_driver):
    erase_range_cmd = EraseRangeShellCommand(mock_ssd_driver, start_lba, end_lba)

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
    erase_range_cmd = EraseRangeShellCommand(mock_ssd_driver, start_lba, end_lba)

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
    erase_range_cmd = EraseRangeShellCommand(mock_ssd_driver, start_lba, end_lba)

    assert not erase_range_cmd.validate()


@pytest.mark.parametrize("start_lba, end_lba, error_arg", [
    ('100', '1', 1),
    ('-1', '10', 1),
    ('가나다', '10', 1),
    ('5', '가다', 1)
])
def test_erase_range_파라미터_초과(start_lba, end_lba, error_arg, mock_ssd_driver):
    erase_range_cmd = EraseRangeShellCommand(mock_ssd_driver, start_lba, end_lba, error_arg)

    assert not erase_range_cmd.validate()


def test_erase_range_파라미터_부족(mock_ssd_driver):
    erase_range_cmd = EraseRangeShellCommand(mock_ssd_driver)

    assert not erase_range_cmd.validate()
