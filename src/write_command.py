from src.command_action import CommandAction


class WriteCommand(CommandAction):
    ERROR_UNVALIDATED = 'Validation Error'
    VALUE_PREFIX = '0x'
    command_name: str = 'write'

    def __init__(self, ssd_driver, *args):
        super().__init__(ssd_driver, *args)
        self._value: str = None
        self._address: int = None

    def run(self) -> None:
        if self.validate() is False:
            raise ValueError(self.ERROR_UNVALIDATED)

        self._ssd_driver.write(self._address, self._value)

    def validate(self) -> bool:
        if len(self._arguments) != 2:
            return False

        self._address, self._value = self._arguments

        if not isinstance(self._address, int) or not 0 <= self._address <= 99:
            return False

        if self.validate_value() is False:
            return False

        return True

    def validate_value(self):
        if (not isinstance(self._value, str) or
                len(self._value) != 10 or
                not self._value.startswith(self.VALUE_PREFIX)):
            return False

        for bit in self._value.strip(self.VALUE_PREFIX):
            if not 'A' <= bit <= 'F' and not '0' <= bit <= '9':
                return False
