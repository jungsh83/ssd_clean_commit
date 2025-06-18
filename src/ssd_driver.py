import subprocess
from pathlib import Path

class ReadException(Exception):
    __module__ = "builtins"

class WriteException(Exception):
    __module__ = "builtins"

class SSDDriver:
    COMMAND_PATH = Path(__file__).parent / "ssd.py"
    OUTPUT_TXT_PATH = Path(__file__).parent.parent / "data/ssd_output.txt"

    def __init__(self):
        pass

    def read(self, lba: int) -> str:
        """
        system call 날려도 되고, subprocess를 날려서 돌려도 됩니다.
        별개의 프로세스로 돌아가게 만든다.
        :param lba: 주소
        :return: 데이터
        :raise 'ERROR" return 받으면 ReadException 처리
        """

        # system call
        cp = subprocess.run(["python", self.COMMAND_PATH, 'R', str(lba)])
        if cp.returncode != 0:
            raise ReadException("Non-zero exit code has been returned.")

        # read output_file
        out = self.OUTPUT_TXT_PATH.read_text().strip()

        if out == "ERROR":
            raise ReadException("ERROR")

        return out

    def write(self, lba: int, value: str) -> None:
        """
        system call 날려도 되고, subprocess를 날려서 돌려도 됩니다.
        별개의 프로세스로 돌아가게 만든다.
        :param lba:
        :param value:
        :raise 'ERROR" return 받으면 WriteException 처리
        """

        # system call
        cp = subprocess.run(["python", self.COMMAND_PATH, 'W', str(lba), str(value)])
        if cp.returncode != 0:
            raise ReadException("Non-zero exit code has been returned.")

        # read output_file
        out = self.OUTPUT_TXT_PATH.read_text().strip()

        if out == "ERROR":
            raise WriteException("ERROR")

        return
