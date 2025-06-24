from src.decorators import log_call
from src.shell_commands.shell_command import ShellCommand, InvalidArgumentException
from ..data_dict import *
from ...logger import LogLevel


class EraseShellCommand(ShellCommand):
    command_name: str = 'erase'
    _description = 'Erase value from LBA with size'
    _usage = 'erase <LBA: int [0-99]> <SIZE: int ["-2,147,483,648" - "2,147,483,647"]'
    _author = 'Gunam Kwon'
    _alias: list[str] = []

    @log_call(level=LogLevel.INFO)
    def __init__(self, ssd_driver, *args):
        super().__init__(ssd_driver, *args)
        self._input_lba: str = INIT_VAL_STR
        self._input_size: str = INIT_VAL_STR

    @log_call(level=LogLevel.INFO)
    def execute(self):
        if not self.validate():
            raise InvalidArgumentException(self._get_exception_string())

        start_lba, end_lba = self._calculate_lba_range()
        size = self._calculate_size(start_lba, end_lba)

        if size == 0:
            self._ssd_driver.erase(start_lba, size)
        else:
            total_size = size
            for offset in range(0, total_size, MAX_ERASE_LEN_ON_SSD_DRIVER):
                cmd_size = min(MAX_ERASE_LEN_ON_SSD_DRIVER, total_size - offset)
                self._ssd_driver.erase(start_lba + offset, cmd_size)

        return DONE_TEXT

    def validate(self) -> bool:
        if len(self._arguments) != VALID_ARGUMENT_RANGE:
            return False

        self._input_lba, self._input_size = self._arguments

        if not self._is_int_string(self._input_lba) or not self._is_int_string(self._input_size):
            return False

        if not LBA_START_INDEX <= int(self._input_lba) < LBA_COUNT:
            return False

        return True

    def _get_exception_string(self) -> str:
        return f"{self.command_name} takes {VALID_ARGUMENT_RANGE} arguments, but got {self._arguments}."

    def _calculate_lba_range(self) -> (int, int):
        lba, size = int(self._input_lba), int(self._input_size)

        if size == 0:
            start_lba, end_lba = lba, INVALID_LBA
        elif size > 0:
            start_lba = lba
            end_lba = min(lba + size - 1, LBA_COUNT - 1)
        else:
            end_lba = lba
            start_lba = max(lba + size + 1, LBA_START_INDEX)

        return start_lba, end_lba

    @staticmethod
    def _calculate_size(start, end):
        if end == INVALID_LBA:
            return 0

        return end - start + 1

    @staticmethod
    def _is_int_string(s: str) -> bool:
        try:
            int(s)
            return True
        except ValueError:
            return False
