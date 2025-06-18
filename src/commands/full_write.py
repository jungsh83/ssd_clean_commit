from src.commands.command_action import CommandAction


class FullWriteCommand(CommandAction):
    ERROR_UNVALIDATED = 'Validation Error'
    VALUE_PREFIX = '0x'
    command_name = ['fullwrite']

    def __init__(self, ssd_driver, *args):
        super().__init__(ssd_driver, *args)
        self._value = None

    def run(self) -> None:
        if not self.validate():
            raise ValueError(self.ERROR_UNVALIDATED)

        for address in range(100):
            self._ssd_driver.write(address, self._value)

    def validate(self) -> bool:
        if len(self._arguments) != 1:
            return False

        self._value = self._arguments[0]

        return self.validate_value()

    def validate_value(self):
        if (not isinstance(self._value, str) or
                len(self._value) != 10 or
                not self._value.startswith(self.VALUE_PREFIX)):
            return False

        for bit in self._value.strip(self.VALUE_PREFIX):
            if not 'A' <= bit <= 'F' and not '0' <= bit <= '9':
                return False

        return True
