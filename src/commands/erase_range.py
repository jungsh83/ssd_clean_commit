from src.commands.command_action import CommandAction, InvalidArgumentException
from src.ssd import VirtualSSD


class EraseRangeCommand(CommandAction):
    command_name: str = 'erase_range'
    _description = 'erase value from range of LBAs'
    _usage = 'erase_range <start_LBA: int [0-99]> <end_LBA: int [0-99]>'
    _author = 'Gunam Kwon'
    _alias = []

    VALID_ARGUMENT_LEN = 2

    def __init__(self, ssd_driver, *args):
        super().__init__(ssd_driver, *args)
        self._end_lba = None
        self._start_lba = None

    def run(self) -> None:
        if not self.validate():
            raise InvalidArgumentException(self.get_exception_string())

        start_lba, end_lba = self._get_lba_range()

    def _get_lba_range(self) -> (int, int):
        start_lba, end_lba = int(self._start_lba), int(self._end_lba)

        start_lba, end_lba = (end_lba, start_lba) if start_lba > end_lba else (start_lba, end_lba)

        return start_lba, end_lba

    @staticmethod
    def _get_size(start_lba: int, end_lba: int) -> int:
        return end_lba - start_lba + 1

    def validate(self) -> bool:
        if len(self._arguments) != self.VALID_ARGUMENT_LEN:
            return False

        self._start_lba, self._end_lba = self._arguments

        if not self._start_lba.isdigit() or not self._end_lba.isdigit():
            return False

        if (not VirtualSSD.LBA_START_INDEX <= int(self._start_lba) < VirtualSSD.LBA_COUNT or
                not VirtualSSD.LBA_START_INDEX <= int(self._end_lba) < VirtualSSD.LBA_COUNT):
            return False

        return True

    def get_exception_string(self):
        return f"{self.command_name} takes {self.VALID_ARGUMENT_LEN} arguments, but got {self._arguments}."
