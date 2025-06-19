import pytest

from src.commands.flush import FlushCommand
from src.ssd_driver import SSDDriver


@pytest.fixture
def mock_ssd_driver(mocker):
    return mocker.Mock(spec=SSDDriver)


def test_flush_command_성공(mock_ssd_driver):
    flush_cmd = FlushCommand(mock_ssd_driver)

    flush_cmd.run()

    mock_ssd_driver.flush.assert_called_once()


@pytest.mark.parametrize("error_arg", ['100', '-1', "가나다", "0.1"])
def test_flush_command_파라미터_초과(error_arg, mock_ssd_driver):
    flush_cmd = FlushCommand(mock_ssd_driver, error_arg)

    assert not flush_cmd.validate()
