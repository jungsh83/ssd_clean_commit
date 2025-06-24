from src.shell_commands.shell_command import ShellCommand, InvalidArgumentException
from src.shell_commands.data_dict import MAX_ERASE_LEN_ON_SSD_DRIVER, LBA_START_INDEX, LBA_COUNT, VALID_ARGUMENT_RANGE
from src.decorators import log_call
from src.logger import LogLevel


class EraseRangeShellCommand(ShellCommand):
    command_name: str = 'erase_range'
    _description = 'erase value from input range of LBAs'
    _usage = 'erase_range <start_LBA: int [0-99]> <end_LBA: int [0-99]>'
    _author = 'Gunam Kwon'
    _alias = []

    def __init__(self, ssd_driver, *args):
        super().__init__(ssd_driver, *args)
        self._end_lba = None
        self._start_lba = None

    @log_call(level=LogLevel.INFO)
    def execute(self) -> None:
        if not self.validate():
            raise InvalidArgumentException(self._get_exception_string())

        start_lba, end_lba = self._get_lba_range()
        size = self._get_size(start_lba, end_lba)

        total_size = size
        for offset in range(0, total_size, MAX_ERASE_LEN_ON_SSD_DRIVER):
            cmd_size = min(MAX_ERASE_LEN_ON_SSD_DRIVER, total_size - offset)
            self._ssd_driver.erase(start_lba + offset, cmd_size)

        return DONE_TEXT

    def _get_lba_range(self) -> (int, int):
        start_lba, end_lba = int(self._start_lba), int(self._end_lba)

        start_lba, end_lba = (end_lba, start_lba) if start_lba > end_lba else (start_lba, end_lba)

        return start_lba, end_lba

    @staticmethod
    def _get_size(start_lba: int, end_lba: int) -> int:
        return end_lba - start_lba + 1

    def validate(self) -> bool:
        if len(self._arguments) != VALID_ARGUMENT_RANGE:
            return False

        self._start_lba, self._end_lba = self._arguments

        if not self._start_lba.isdigit() or not self._end_lba.isdigit():
            return False

        if (not LBA_START_INDEX <= int(self._start_lba) < LBA_COUNT or
                not LBA_START_INDEX <= int(self._end_lba) < LBA_COUNT):
            return False

        return True

    def _get_exception_string(self):
        return f"{self.command_name} takes {VALID_ARGUMENT_RANGE} arguments, but got {self._arguments}."
