from src.command_action import CommandAction


class FullWriteCommand(CommandAction):
    command_name = ['fullwrite']

    def __init__(self, ssd_driver, *args):
        super().__init__(ssd_driver, *args)
        self._value = None

    def run(self) -> None:
        if self.validate() is False:
            raise ValueError()

        for address in range(100):
            self._ssd_driver.write(address, self._value)

    def validate(self) -> bool:
        if len(self._arguments) != 1:
            return False

        self._value = self._arguments[0]

        if not isinstance(self._value, str):
            return False

        if len(self._value) != 10:
            return False

        for v in self._value.strip('0x'):
            if not 'A' <= v <= 'F' and not '0' <= v <= '9':
                return False

        return True
