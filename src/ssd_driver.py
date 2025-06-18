import subprocess
from pathlib import Path

VALID_RETURN_CODE = 0

class ReadException(Exception):
    __module__ = "builtins"


class WriteException(Exception):
    __module__ = "builtins"


class SSDDriver:
    VENV_PYTHON_PATH = Path(__file__).parent.parent / ".venv/Scripts/python.exe"
    COMMAND_PATH = Path(__file__).parent / "ssd.py"
    OUTPUT_TXT_PATH = Path(__file__).parent.parent / "data/ssd_output.txt"
    READ_TOKEN = 'R'
    WRITE_TOKEN = 'W'

    def read(self, lba: int) -> str:
        """
        지정된 lba 위치의 SSD Data를 읽어 값을 반환 한다.

        :param lba: 주소
        :return: 4byte 16진수 형식의 문자열 "e.g 0x00000000"
        :raise 'ERROR" return 받으면 ReadException 처리
        """

        # system call
        cp = subprocess.run([self.VENV_PYTHON_PATH, self.COMMAND_PATH, self.READ_TOKEN, str(lba)])
        if cp.returncode != VALID_RETURN_CODE:
            raise ReadException("Non-zero exit code has been returned.")

        # read output_file
        out = self.OUTPUT_TXT_PATH.read_text().strip()

        if out == "ERROR":
            raise ReadException("ERROR")

        return out

    def write(self, lba: int, value: str) -> None:
        """
        lba 위치에 value 값을  SSD Data에 기록 한다.

        :param lba: SSD의 저장 위치 (0~99)
        :param value: 4byte 16진수 형식의 문자열 "e.g 0x00000000"
        :raise 'ERROR" return 받으면 WriteException 처리
        """

        # system call
        cp = subprocess.run([self.VENV_PYTHON_PATH, self.COMMAND_PATH, self.WRITE_TOKEN, str(lba), str(value)])
        if cp.returncode != VALID_RETURN_CODE:
            raise WriteException("Non-zero exit code has been returned.")

        # read output_file
        out = self.OUTPUT_TXT_PATH.read_text().strip()

        if out == "ERROR":
            raise WriteException("ERROR")

        return
