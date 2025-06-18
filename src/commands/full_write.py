from src.commands.command_action import CommandAction, InvalidArgumentException


class FullWriteCommand(CommandAction):
    command_name: str = 'fullwrite'
    _description = 'Show list of available commands.'
    _usage = 'fullwrite <value: hex32bit, e.g. 0x12345678>'
    _author = 'Gunam Kwon'
    _alias = []

    VALID_ARGUMENT_LEN = 1

    def __init__(self, ssd_driver, *args):
        super().__init__(ssd_driver, *args)
        self._value = None

    def run(self) -> None:
        if not self.validate():
            raise InvalidArgumentException(self.get_exception_string(len(self._arguments)))

        for address in range(100):
            self._ssd_driver.write(address, self._value)

    def validate(self) -> bool:
        if len(self._arguments) != self.VALID_ARGUMENT_LEN:
            return False

        self._value = self._arguments[0]
        return True

    def get_exception_string(self, error_arguments_len):
        return f"{self.command_name} takes {self.VALID_ARGUMENT_LEN} arguments, but got {error_arguments_len}."
