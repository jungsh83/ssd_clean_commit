import pytest
from pytest_mock import MockerFixture

from src.partial_lba_write import PartialLBAWrite


def test_partial_lba_write_validate_호출_정상(mocker: MockerFixture):
    ssd = mocker.Mock()
    sut = PartialLBAWrite(ssd_driver=ssd)
    actual = sut.validate()

    assert actual
