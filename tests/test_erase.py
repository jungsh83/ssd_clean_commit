import pytest

from src import EraseCommand
from src.commands.command_action import InvalidArgumentException
from src.ssd_driver import SSDDriver


@pytest.fixture
def ssd_driver_mock(mocker):
    return mocker.Mock(spec=SSDDriver)


@pytest.mark.parametrize("lba, size, expected_call_count", [
    ('5', '0', 1),
    ('98', '10', 1),
    ('50', '100', 5),
    ('0', '999', 10),
    ('10', '-10', 1),
    ('5', '-2', 1),
    ('5', '1', 1),
    ('5', '-1', 1),
    ('50', '-100', 6),
    ('85', '100', 2)
])
def test_erase_command_call_count_확인(lba, size, expected_call_count, ssd_driver_mock):
    erase_cmd = EraseCommand(ssd_driver_mock, lba, size)

    erase_cmd.run()

    assert ssd_driver_mock.erase.call_count == expected_call_count


@pytest.mark.parametrize("lba, size, expected_start_lba, expected_end_lba", [
    ('98', '10', 98, 99),
    ('50', '100', 50, 99),
    ('0', '999', 0, 99),
    ('10', '-10', 1, 10),
    ('5', '-2', 4, 5),
    ('5', '1', 5, 5),
    ('5', '-1', 5, 5),
    ('50', '-100', 0, 50),
    ('85', '100', 85, 99),
    ('5', '0', 5, -1)
])
def test_erase_command_start_end_확인(lba, size, expected_start_lba, expected_end_lba, ssd_driver_mock):
    erase_cmd = EraseCommand(ssd_driver_mock, lba, size)

    erase_cmd.run()
    start_lba, end_lba = erase_cmd._calculate_lba_range()

    assert erase_cmd.validate()
    assert (start_lba, end_lba) == (expected_start_lba, expected_end_lba)


@pytest.mark.parametrize("lba, size, expected_size", [
    ('98', '10', 2),
    ('50', '100', 50),
    ('0', '999', 100),
    ('10', '-10', 10),
    ('5', '-2', 2),
    ('5', '1', 1),
    ('5', '-1', 1),
    ('50', '-100', 51),
    ('85', '100', 15),
    ('5', '0', 0)
])
def test_erase_command_size_계산(lba, size, expected_size, ssd_driver_mock):
    erase_cmd = EraseCommand(ssd_driver_mock, lba, size)

    erase_cmd.run()
    start_lba, end_lba = erase_cmd._calculate_lba_range()

    assert erase_cmd._calculate_size(start_lba, end_lba) == expected_size


@pytest.mark.parametrize("lba, size", [
    ('100', '10'),
    ('-1', '10'),
    ('가나다', '10'),
    ('5', "가다"),
])
def test_erase_command_유효성_검사(lba, size, ssd_driver_mock):
    erase_cmd = EraseCommand(ssd_driver_mock, lba, size)

    with pytest.raises(InvalidArgumentException):
        erase_cmd.run()

    assert not erase_cmd.validate()


@pytest.mark.parametrize("lba, size, error_argument", [
    (100, 10, 1),
    (-1, 10, 2),
    ("가나다", 10, 3),
    (5, "가다", 4)
])
def test_erase_command_파라미터_초과(lba, size, error_argument, ssd_driver_mock):
    erase_cmd = EraseCommand(ssd_driver_mock, lba, size, error_argument)

    with pytest.raises(InvalidArgumentException):
        erase_cmd.run()

    assert not erase_cmd.validate()


def test_erase_command_파라미터_부족(ssd_driver_mock):
    erase_cmd = EraseCommand(ssd_driver_mock)

    with pytest.raises(InvalidArgumentException):
        erase_cmd.run()

    assert not erase_cmd.validate()
