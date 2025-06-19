import pytest

from src.ssd_commands.ssd_command_action import SSDCommand, InvalidArgumentException
from src.ssd_commands.ssd_command_write import SSDCommandWrite

@pytest.fixture
def fake_mgr(mocker):
    mgr = mocker.Mock()
    mgr.write = mocker.Mock()
    return mgr


@pytest.mark.parametrize(
    "lba, value",
    [
        (0,  "0xABCDEF12"),
        (50, "0x12345678"),
        (99, "0xFFFFFFFF"),
    ],
)
def test_write_ok(fake_mgr, lba, value):
    cmd = SSDCommandWrite(fake_mgr, str(lba), value)
    assert cmd.validate() is True
    assert cmd.run() == "Done"
    fake_mgr.write.assert_called_once_with(lba, value.upper())


@pytest.mark.parametrize(
    "args",
    [
        (),                              # 인자 없음
        ("10",),                         # 1개
        ("10", "0x1234"),                # 길이 오류
        ("10", "ABCDEF12"),              # 0x 없음
        ("-1", "0x12345678"),            # LBA 음수
        ("100", "0x12345678"),           # 범위 초과
    ],
)
def test_write_invalid(fake_mgr, args):
    cmd = SSDCommandWrite(fake_mgr, *args)
    with pytest.raises(InvalidArgumentException):
        cmd.run()
    fake_mgr.write.assert_not_called()


