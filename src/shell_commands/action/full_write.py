from src.shell_commands.shell_command_action import ShellCommandAction, InvalidArgumentException
from ..data_dict import *


class FullWriteShellCommand(ShellCommandAction):
    command_name: str = 'fullwrite'
    _description = 'write value to all of LBAs'
    _usage = 'fullwrite <value: hex32bit, e.g. 0x12345678>'
    _author = 'Gunam Kwon'
    _alias = []

    def __init__(self, ssd_driver, *args):
        super().__init__(ssd_driver, *args)
        self._value = None

    def run(self) -> None:
        if not self.validate():
            raise InvalidArgumentException(self.get_exception_string())

        for lba in range(LBA_COUNT):
            self._ssd_driver.write(lba, self._value)

    def validate(self) -> bool:
        if len(self._arguments) != VALID_ARGUMENT_SINGLE:
            return False

        self._value = self._arguments[0]
        return True

    def get_exception_string(self):
        return f"{self.command_name} takes {VALID_ARGUMENT_SINGLE} arguments, but got {self._arguments}."
