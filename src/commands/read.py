from src.commands.command_action import CommandAction, InvalidArgumentException


class ReadCommand(CommandAction):
    command_name: str = 'read'
    _description = 'Show list of available commands.'
    _usage = 'read'
    _author = 'Gunam Kwon'
    _alias = []

    def __init__(self, ssd_driver, *args):
        super().__init__(ssd_driver, *args)
        self._address = None

    def run(self) -> str:
        if not self.validate():
            raise InvalidArgumentException()

        return self.print_output(self._address, self._ssd_driver.read(self._address))

    def validate(self) -> bool:
        if len(self._arguments) != 1:
            return False

        self._address: int = self._arguments[0]

        return True

    @staticmethod
    def print_output(address, value):
        return f'LBA {address} : {value}'
