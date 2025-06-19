import pytest
import tempfile
from pathlib import Path

from src.shell import runner_mode
from src.commands.command_action import CommandAction


class DummyCommand(CommandAction):
    command_name = "1_dummy"
    _alias = []

    def validate(self):
        return True

    def run(self):
        return "PASS"


@pytest.fixture(autouse=True)
def register_dummy():
    CommandAction.registry["1_dummy"] = DummyCommand
    yield
    CommandAction.registry.pop("1_dummy", None)


def test_runner_성공(monkeypatch, capsys):
    # 임시 파일에 유효한 커맨드 작성
    with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".txt") as tmp:
        tmp.write("1_dummy\n")
        tmp_path = tmp.name

    # sys.exit을 막고 exit code 확인
    with pytest.raises(SystemExit) as e:
        runner_mode(tmp_path)

    assert e.value.code == 0  # PASS인 경우 정상 종료
    output = capsys.readouterr().out
    assert "PASS" in output

    Path(tmp_path).unlink()


def test_runner_테스트케이스_실패(monkeypatch, capsys):
    class FailingCommand(CommandAction):
        command_name = "1_fail"
        _alias = []

        def validate(self):
            return True

        def run(self):
            return "FAIL"

    CommandAction.registry["1_fail"] = FailingCommand

    with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".txt") as tmp:
        tmp.write("1_fail\n")
        tmp_path = tmp.name

    with pytest.raises(SystemExit) as e:
        runner_mode(tmp_path)

    assert e.value.code == 1  # FAIL인 경우 비정상 종료
    output = capsys.readouterr().out
    assert "FAIL" in output

    Path(tmp_path).unlink()
    CommandAction.registry.pop("1_fail", None)


def test_runner_mode_유효하지않은_명령어(monkeypatch, capsys):
    with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".txt") as tmp:
        tmp.write("INVALID_COMMAND\n")
        tmp_path = tmp.name

    with pytest.raises(SystemExit) as e:
        runner_mode(tmp_path)

    assert e.value.code == 1
    output = capsys.readouterr().out
    assert "INVALID COMMAND" in output

    Path(tmp_path).unlink()
