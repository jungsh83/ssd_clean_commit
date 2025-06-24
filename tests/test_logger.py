import shutil
import pytest
from pathlib import Path
from src.logger import LoggerSingleton, _CustomLogger


@pytest.fixture(scope="function")
def fixed_log_dir(monkeypatch):
    test_logs = Path(__file__).parent / "test_logger_temp" / "logs"

    if test_logs.exists():
        shutil.rmtree(test_logs)
    test_logs.mkdir(parents=True, exist_ok=True)

    monkeypatch.setattr(_CustomLogger, "LOG_DIR", test_logs)
    monkeypatch.setattr(_CustomLogger, "LOG_FILE", test_logs / "latest.log")
    LoggerSingleton._instance = None  # 싱글톤 리셋

    yield test_logs

    shutil.rmtree(test_logs.parent)


def test_logger_파일생성되는지_각파일이10kB넘지않는지(fixed_log_dir):
    logger = LoggerSingleton.get_logger()
    message = "X" * 1024  # 1kB

    for _ in range(21):
        logger.info(message)

    log_files = list(fixed_log_dir.glob("until_*.log"))
    zip_files = list(fixed_log_dir.glob("until_*.zip"))
    latest_log = fixed_log_dir / "latest.log"

    assert len(log_files) >= 1, "until_*.log 없음"
    assert len(zip_files) >= 1, "zip 백업 없음"
    assert latest_log.exists(), "latest.log 없음"

    max_size_with_margin = 12 * 1024  # 10KB

    for log_file in log_files:
        assert log_file.stat().st_size <= max_size_with_margin, f"{log_file.name} 크기 초과"

    for zip_file in zip_files:
        assert zip_file.stat().st_size <= max_size_with_margin, f"{zip_file.name} 크기 초과"

    assert latest_log.stat().st_size <= max_size_with_margin, "latest.log 너무 큼 (rotate 안 됨)"


def test_logger_log_잘나오는지(fixed_log_dir):
    logger = LoggerSingleton.get_logger()

    logger.info("info")
    logger.debug("debug")
    logger.error("error")

    latest_log = fixed_log_dir / "latest.log"

    assert latest_log.exists(), "latest.log 파일이 존재하지 않음"

    log_content = latest_log.read_text(encoding="utf-8")

    assert "INFO" in log_content, "'INFO' 로그가 기록되지 않음"
    assert "DEBUG" in log_content, "'DEBUG' 로그가 기록되지 않음"
    assert "ERROR" in log_content, "'ERROR' 로그가 기록되지 않음"


def test_logger_builtin_print_패치되는지(fixed_log_dir):
    logger = LoggerSingleton.get_logger()

    print("builtin_print_patched")

    latest_log = fixed_log_dir / "latest.log"

    assert latest_log.exists(), "latest.log 파일이 존재하지 않음"

    log_content = latest_log.read_text(encoding="utf-8")

    assert "builtin_print_patched" in log_content, "bulit-in print 함수의 출력이 패치되지 않음"
