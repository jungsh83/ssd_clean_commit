import io
import sys

import pytest
from pytest_mock import MockerFixture
from unittest.mock import call

from src.partial_lba_write import PartialLBAWrite


def test_partial_lba_write_validate_호출_정상(mocker: MockerFixture):
    assert PartialLBAWrite(ssd_driver=mocker.Mock()).validate()

def test_partial_lba_write_validate_호출시_인자값_넣어서_실패(mocker: MockerFixture):
    assert not PartialLBAWrite(mocker.Mock(), 3, "0x00000000", ).validate()

def test_partial_lba_write_name_클래스변수_리스트_확인(mocker: MockerFixture):
    assert PartialLBAWrite.command_name == ['2_PartialLBAWrite', '2_']


def test_partial_lba_write_name_run_write_150번_수행_확인(mocker: MockerFixture):
    ssd_driver = mocker.Mock()
    PartialLBAWrite(ssd_driver=ssd_driver).run()

    assert ssd_driver.write.call_count == 150


def test_partial_lba_write_name_run_write_random_처리_확인(mocker: MockerFixture):
    ssd_driver = mocker.Mock()
    PartialLBAWrite(ssd_driver=ssd_driver).run()

    assert ssd_driver.write.call_args_list[0].args[0] != \
           ssd_driver.write.call_args_list[1].args[0] != \
           ssd_driver.write.call_args_list[2].args[0] != \
           ssd_driver.write.call_args_list[3].args[0] != \
           ssd_driver.write.call_args_list[4].args[0]


@pytest.mark.skip
def test_partial_lba_write_name_run_read_150번_수행_확인(mocker: MockerFixture):
    ssd_driver = mocker.Mock()
    PartialLBAWrite(ssd_driver=ssd_driver).run()

    assert ssd_driver.read.call_count == 150


@pytest.mark.skip
def test_partial_lba_write_name_run_read_success(mocker: MockerFixture):
    output = io.StringIO()
    original = sys.stdout
    sys.stdout = output
    ssd_driver = mocker.Mock()
    PartialLBAWrite(ssd_driver=ssd_driver).run()

    assert output.getvalue() == "PASS"
    sys.stdout = original


@pytest.mark.skip
def test_partial_lba_write_name_run_read_fail(mocker: MockerFixture):
    output = io.StringIO()
    original = sys.stdout
    sys.stdout = output
    ssd_driver = mocker.Mock()
    PartialLBAWrite(ssd_driver=ssd_driver).run()

    assert output.getvalue() == "FAIL"
    sys.stdout = original
