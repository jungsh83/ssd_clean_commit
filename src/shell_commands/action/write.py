from src.decorators import log_call
from src.shell_commands.shell_command import ShellCommand, InvalidArgumentException
from src.shell_commands.data_dict import VALID_ARGUMENT_RANGE, INIT_VAL_INT, INIT_VAL_STR, DONE_TEXT
from src.logger import LogLevel


class WriteShellCommand(ShellCommand):
    command_name: str = 'write'
    _description = 'write value to LBA'
    _usage = 'write <LBA: int [0-99]> <value: hex32bit, e.g. 0x12345678>'
    _author = 'Gunam Kwon'
    _alias = []

    @log_call(level=LogLevel.INFO)
    def __init__(self, ssd_driver, *args):
        super().__init__(ssd_driver, *args)
        self._value: str = INIT_VAL_STR
        self._lba: int = INIT_VAL_INT

    @log_call(level=LogLevel.INFO)
    def execute(self) -> str:
        if not self.validate():
            raise InvalidArgumentException(self._get_exception_string())

        self._ssd_driver.write(self._lba, self._value)
        return DONE_TEXT

    def validate(self) -> bool:
        if len(self._arguments) != VALID_ARGUMENT_RANGE:
            return False

        self._lba, self._value = self._arguments

        return True

    def _get_exception_string(self):
        return f"{self.command_name} takes {VALID_ARGUMENT_RANGE} arguments, but got {self._arguments}."
