from src.commands.command_action import CommandAction, InvalidArgumentException


class EraseRangeCommand(CommandAction):
    command_name: str = 'erase_range'
    _description = 'erase value from range of LBAs'
    _usage = 'erase_range <start_LBA: int [0-99]> <end_LBA: int [0-99]>'
    _author = 'Gunam Kwon'
    _alias = []

    VALID_ARGUMENT_LEN = 2

    def __init__(self, ssd_driver, *args):
        super().__init__(ssd_driver, *args)

    def run(self) -> None:
        if not self.validate():
            raise InvalidArgumentException(self.get_exception_string())

        start_lba, end_lba = self._get_lba_range()

    def _get_lba_range(self) -> (int, int):
        start_lba, end_lba = self._arguments

        start_lba, end_lba = (end_lba, start_lba) if int(start_lba) > int(end_lba) else (start_lba, end_lba)

        return int(start_lba), int(end_lba)

    def validate(self) -> bool:
        return len(self._arguments) == self.VALID_ARGUMENT_LEN

    def get_exception_string(self):
        return f"{self.command_name} takes {self.VALID_ARGUMENT_LEN} arguments, but got {self._arguments}."
