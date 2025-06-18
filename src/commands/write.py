from src.commands.command_action import CommandAction, InvalidArgumentException


class WriteCommand(CommandAction):
    command_name: str = 'write'
    _description = 'Show list of available commands.'
    _usage = 'fullwrite'
    _author = 'Gunam Kwon'
    _alias = []

    def __init__(self, ssd_driver, *args):
        super().__init__(ssd_driver, *args)
        self._value: str = None
        self._address: int = None

    def run(self) -> None:
        if not self.validate():
            raise InvalidArgumentException()

        self._ssd_driver.write(self._address, self._value)

    def validate(self) -> bool:
        if len(self._arguments) != 2:
            return False

        self._address, self._value = self._arguments

        return True
