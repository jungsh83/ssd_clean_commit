from src.decorators import log_call
from src.shell_commands.shell_command_action import ShellCommandAction, InvalidArgumentException
from ..data_dict import VALID_ARGUMENT_RANGE, INIT_VAL_INT, INIT_VAL_STR


class WriteShellCommand(ShellCommandAction):
    command_name: str = 'write'
    _description = 'write value to LBA'
    _usage = 'write <LBA: int [0-99]> <value: hex32bit, e.g. 0x12345678>'
    _author = 'Gunam Kwon'
    _alias = []


    @log_call(level="INFO")
    def __init__(self, ssd_driver, *args):
        super().__init__(ssd_driver, *args)
        self._value: str = INIT_VAL_STR
        self._lba: int = INIT_VAL_INT

    @log_call(level="INFO")
    def run(self) -> str:
        if not self.validate():
            raise InvalidArgumentException(self.get_exception_string())

        self._ssd_driver.write(self._lba, self._value)
        return "Done"

    def validate(self) -> bool:
        if len(self._arguments) != 2:
            return False

        self._lba, self._value = self._arguments

        return True

    def get_exception_string(self):
        return f"{self.command_name} takes {VALID_ARGUMENT_RANGE} arguments, but got {self._arguments}."
