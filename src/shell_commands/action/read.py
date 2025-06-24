from src.decorators import log_call
from src.shell_commands.shell_command import ShellCommand, InvalidArgumentException
from ..data_dict import VALID_ARGUMENT_SINGLE, INIT_VAL_INT
from ...logger import LogLevel


class ReadShellCommand(ShellCommand):
    command_name: str = 'read'
    _description = 'read value from LBA'
    _usage = 'read <LBA: int [0-99]>'
    _author = 'Gunam Kwon'
    _alias = []

    @log_call(level=LogLevel.INFO)
    def __init__(self, ssd_driver, *args):
        super().__init__(ssd_driver, *args)
        self._lba: int = INIT_VAL_INT

    @log_call(level=LogLevel.INFO)
    def execute(self) -> str:
        if not self.validate():
            raise InvalidArgumentException(self.get_exception_string())

        return self.print_output(self._lba, self._ssd_driver.read(self._lba))

    def validate(self) -> bool:
        if len(self._arguments) != VALID_ARGUMENT_SINGLE:
            return False

        self._lba: int = self._arguments[0]

        return True

    @staticmethod
    def print_output(lba, value):
        return f'LBA {lba} : {value}'

    def get_exception_string(self):
        return f"{self.command_name} takes {VALID_ARGUMENT_SINGLE} arguments, but got {self._arguments}."
