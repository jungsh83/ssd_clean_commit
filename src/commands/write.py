from src.commands.command_action import CommandAction, InvalidArgumentException


class WriteCommand(CommandAction):
    command_name: str = 'write'
    _description = 'Show list of available commands.'
    _usage = 'write <LBA: int [0-99]> <value: hex32bit, e.g. 0x12345678>'
    _author = 'Gunam Kwon'
    _alias = []

    VALID_ARGUMENT_LEN = 2

    def __init__(self, ssd_driver, *args):
        super().__init__(ssd_driver, *args)
        self._value: str = None
        self._address: int = None

    def run(self) -> None:
        if not self.validate():
            raise InvalidArgumentException(self.get_exception_string(len(self._arguments)))

        self._ssd_driver.write(self._address, self._value)

    def validate(self) -> bool:
        if len(self._arguments) != 2:
            return False

        self._address, self._value = self._arguments

        return True

    def get_exception_string(self, error_arguments_len):
        return f"{self.command_name} takes {self.VALID_ARGUMENT_LEN} arguments, but got {error_arguments_len}."
