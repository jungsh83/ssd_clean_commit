import subprocess
from pathlib import Path
from src.decorators import log_call
from .data_dict import VALID_RETURN_CODE


class ReadException(Exception):
    __module__ = "builtins"


class WriteException(Exception):
    __module__ = "builtins"


class EraseException(Exception):
    __module__ = "builtins"


class FlushException(Exception):
    __module__ = "builtins"


class SSDDriver:
    _instance = None

    VENV_PYTHON_PATH = Path(__file__).parent.parent / ".venv/Scripts/python.exe"
    COMMAND_PATH = Path(__file__).parent.parent / "ssd.py"
    OUTPUT_TXT_PATH = Path(__file__).parent.parent / "data/ssd_output.txt"
    READ_TOKEN = 'R'
    WRITE_TOKEN = 'W'
    ERASE_TOKEN = 'E'
    FLUSH_TOKEN = 'F'

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @log_call(level="INFO")
    def read(self, lba: int) -> str:
        """
        지정된 lba 위치의 SSD Data를 읽어 값을 반환 한다.

        :param lba: 주소
        :return: 4byte 16진수 형식의 문자열 "e.g 0x00000000"
        :raise 'ERROR" return 받으면 ReadException 처리
        """

        out = self.get_external_output(ReadException, self.READ_TOKEN, str(lba))
        if out == "ERROR":
            raise ReadException("ERROR")
        return out

    @log_call(level="INFO")
    def write(self, lba: int, value: str) -> None:
        """
        lba 위치에 value 값을  SSD Data에 기록 한다.

        :param lba: SSD의 저장 위치 (0~99)
        :param value: 4byte 16진수 형식의 문자열 "e.g 0x00000000"
        :raise 'ERROR" return 받으면 WriteException 처리
        """

        out = self.get_external_output(WriteException, self.WRITE_TOKEN, str(lba), str(value))
        if out == "ERROR":
            raise WriteException("ERROR")

        return

    @log_call(level="INFO")
    def erase(self, lba, size):
        out = self.get_external_output(EraseException, self.ERASE_TOKEN, str(lba), str(size))
        if out == "ERROR":
            raise EraseException("ERROR")

        return

    @log_call(level="INFO")
    def flush(self):
        """
        Flush는 실행 후 결과 확인이 없음으로 Test 코드를 추가하지 않습니다.
        :return:
        """
        self.get_external_output(FlushException, self.FLUSH_TOKEN)
        return

    def get_external_output(self, except_class, action_token, *args):
        cp = subprocess.run(
            [self.VENV_PYTHON_PATH, self.COMMAND_PATH, action_token] + list(args),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if cp.returncode != VALID_RETURN_CODE:
            raise except_class(f"Non-zero exit code has been returned.\nError Message: {cp.stderr}")

        # read output_file
        out = self.OUTPUT_TXT_PATH.read_text().strip()
        return out
