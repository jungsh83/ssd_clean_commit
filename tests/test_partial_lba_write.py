import pytest
from pytest_mock import MockerFixture

from src.shell_commands.shell_command import InvalidArgumentException
from src.shell_commands.script.partial_lba_write import PartialLBAWriteShellCommand


def create_test_value():
    test_value = []
    for i in range(10000001, 10000031):
        for j in range(5):
            test_value.append(f'0x{i}')

    return test_value


def test_partial_lba_write_validate_호출_정상(mocker: MockerFixture):
    assert PartialLBAWriteShellCommand(ssd_driver=mocker.Mock()).validate()


def test_partial_lba_write_validate_호출시_인자값_넣어서_실패(mocker: MockerFixture):
    assert not PartialLBAWriteShellCommand(mocker.Mock(), 3, "0x00000000", ).validate()

def test_partial_lba_write_run_호출시_인자값_넣어서_실패(mocker: MockerFixture):
    with pytest.raises(InvalidArgumentException):
        PartialLBAWriteShellCommand(mocker.Mock(), 3, "0x00000000", ).execute()

def test_partial_lba_write_name_클래스변수_리스트_확인(mocker: MockerFixture):
    assert PartialLBAWriteShellCommand.command_name == '2_PartialLBAWrite'


def test_partial_lba_write_name_run_write_150번_수행_확인(mocker: MockerFixture):
    ssd_driver = mocker.Mock()
    ssd_driver.write.return_value = None
    ssd_driver.read.side_effect = create_test_value()

    PartialLBAWriteShellCommand(ssd_driver=ssd_driver).execute()

    assert ssd_driver.write.call_count == 150


def test_partial_lba_write_name_run_write_random_처리_확인(mocker: MockerFixture):
    ssd_driver = mocker.Mock()
    ssd_driver.write.return_value = None
    ssd_driver.read.side_effect = create_test_value()

    PartialLBAWriteShellCommand(ssd_driver=ssd_driver).execute()

    assert ssd_driver.write.call_args_list[0].args[0] != \
           ssd_driver.write.call_args_list[1].args[0] != \
           ssd_driver.write.call_args_list[2].args[0] != \
           ssd_driver.write.call_args_list[3].args[0] != \
           ssd_driver.write.call_args_list[4].args[0]


def test_partial_lba_write_name_run_read_150번_수행_확인(mocker: MockerFixture):
    ssd_driver = mocker.Mock()
    ssd_driver.write.return_value = None
    ssd_driver.read.side_effect = create_test_value()

    PartialLBAWriteShellCommand(ssd_driver=ssd_driver).execute()

    assert ssd_driver.read.call_count == 150


def test_partial_lba_write_name_run_성공(mocker: MockerFixture):
    ssd_driver = mocker.Mock()
    ssd_driver.write.return_value = None
    ssd_driver.read.side_effect = create_test_value()

    actual = PartialLBAWriteShellCommand(ssd_driver=ssd_driver).execute()

    assert actual == "PASS"


def test_partial_lba_write_name_run_실패(mocker: MockerFixture):
    ssd_driver = mocker.Mock()
    ssd_driver.write.return_value = None
    ssd_driver.read.return_value = "0x00000002"

    actual = PartialLBAWriteShellCommand(ssd_driver=ssd_driver).execute()

    assert actual == "FAIL"
