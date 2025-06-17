import pytest
from pytest_mock import MockerFixture

from src.partial_lba_write import PartialLBAWrite


def test_partial_lba_write_validate_호출_정상(mocker: MockerFixture):
    assert PartialLBAWrite(ssd_driver=mocker.Mock()).validate()

def test_partial_lba_write_name_클래스변수_리스트_확인(mocker: MockerFixture):
    assert PartialLBAWrite.command_name == ['2_PartialLBAWrite', '2_']