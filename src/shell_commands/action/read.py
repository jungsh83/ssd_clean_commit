from src.shell_commands.shell_command_action import ShellCommandAction, InvalidArgumentException


class ReadShellCommand(ShellCommandAction):
    command_name: str = 'read'
    _description = 'read value from LBA'
    _usage = 'read <LBA: int [0-99]>'
    _author = 'Gunam Kwon'
    _alias = []

    VALID_ARGUMENT_LEN = 1

    def __init__(self, ssd_driver, *args):
        super().__init__(ssd_driver, *args)
        self._LBA = None

    def run(self) -> str:
        if not self.validate():
            raise InvalidArgumentException(self.get_exception_string())

        return self.print_output(self._LBA, self._ssd_driver.read(self._LBA))

    def validate(self) -> bool:
        if len(self._arguments) != self.VALID_ARGUMENT_LEN:
            return False

        self._LBA: int = self._arguments[0]

        return True

    @staticmethod
    def print_output(lba, value):
        return f'LBA {lba} : {value}'

    def get_exception_string(self):
        return f"{self.command_name} takes {self.VALID_ARGUMENT_LEN} arguments, but got {self._arguments}."
