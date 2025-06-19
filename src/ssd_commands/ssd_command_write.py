import re
from .ssd_command_action import SSDCommand, InvalidArgumentException
from ..ssd_file_manager import SSDFileManager

HEX32 = re.compile(r"^0x[0-9A-Fa-f]{8}$")
LBA_MIN = SSDFileManager.LBA_START_INDEX
LBA_MAX = SSDFileManager.LBA_START_INDEX + SSDFileManager.LBA_COUNT - 1   # 99

class SSDCommandWrite(SSDCommand):
    command_name = ["write", "w"]
    _description = "Write command to buffer"
    _usage = "write <LBA 0-99> <0xXXXXXXXX>"
    _author = "Sungkyung Woo"

    def validate(self) -> bool:
        if len(self._arguments) != 2:
            return False

        lba_str, value = self._arguments

        # LBA 정수 여부 + 범위 체크
        try:
            lba = int(lba_str)
        except ValueError:
            return False
        if not (LBA_MIN <= lba <= LBA_MAX):
            return False

        # 32-bit hex 형식 체크
        if HEX32.fullmatch(value) is None:
            return False

        return True

    def run(self) -> str:
        if not self.validate():
            raise InvalidArgumentException("Write: invalid arguments")

        lba = int(self._arguments[0])
        value = self._arguments[1].upper()

        self._ssd_file_manager.write(lba, value)   # 이름 맞춰 확인!
        return "Done"