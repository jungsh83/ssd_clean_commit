from src.commands.command_action import CommandAction, InvalidArgumentException


class FullWriteCommand(CommandAction):
    ERROR_UNVALIDATED = 'Validation Error'
    VALUE_PREFIX = '0x'
    command_name = ['fullwrite']

    def __init__(self, ssd_driver, *args):
        super().__init__(ssd_driver, *args)
        self._value = None

    def run(self) -> None:
        if not self.validate():
            raise InvalidArgumentException()

        for address in range(100):
            self._ssd_driver.write(address, self._value)

    def validate(self) -> bool:
        if len(self._arguments) != 1:
            return False

        self._value = self._arguments[0]
        return True
