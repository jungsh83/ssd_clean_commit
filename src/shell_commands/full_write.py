from src.shell_commands.command_action import CommandAction, InvalidArgumentException
from src.ssd_file_manager import SSDFileManager


class FullWriteCommand(CommandAction):
    command_name: str = 'fullwrite'
    _description = 'write value to all of LBAs'
    _usage = 'fullwrite <value: hex32bit, e.g. 0x12345678>'
    _author = 'Gunam Kwon'
    _alias = []

    VALID_ARGUMENT_LEN = 1

    def __init__(self, ssd_driver, *args):
        super().__init__(ssd_driver, *args)
        self._value = None

    def run(self) -> None:
        if not self.validate():
            raise InvalidArgumentException(self.get_exception_string())

        for lba in range(SSDFileManager.LBA_COUNT):
            self._ssd_driver.write(lba, self._value)

    def validate(self) -> bool:
        if len(self._arguments) != self.VALID_ARGUMENT_LEN:
            return False

        self._value = self._arguments[0]
        return True

    def get_exception_string(self):
        return f"{self.command_name} takes {self.VALID_ARGUMENT_LEN} arguments, but got {self._arguments}."
