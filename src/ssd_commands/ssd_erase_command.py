import re
from .ssd_command_action import SSDCommand, InvalidArgumentException
from ..ssd_file_manager import SSDFileManager

LBA_MIN = SSDFileManager.LBA_START_INDEX
LBA_MAX = SSDFileManager.LBA_START_INDEX + SSDFileManager.LBA_COUNT - 1  # 99


class SSDCommandErase(SSDCommand):
    def validate(self) -> bool:
        if len(self._arguments) != 2:
            return False

        lba_str, size_str = self._arguments

        return (
                self._is_valid_unsigned_int_in_range(lba_str, LBA_MIN, LBA_MAX) and
                self._is_valid_unsigned_int_in_range(size_str, 0, 10)
        )

    def _is_valid_unsigned_int_in_range(self, str_var, lower_bound, upper_bound):
        return str_var.isdigit() and lower_bound <= int(str_var) <= upper_bound

    def run(self) -> str:
        if not self.validate():
            raise InvalidArgumentException("Erase: invalid arguments")

        lba = int(self._arguments[0])
        size = int(self._arguments[1])

        self._ssd_file_manager.erase(lba, size)
        return "Done"
