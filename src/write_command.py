from src.command_action import CommandAction


class WriteCommand(CommandAction):
    command_name: list = ['write']

    def __init__(self, ssd_driver, *args):
        super().__init__(ssd_driver, *args)
        self._value: str = None
        self._address: int = None

    def run(self) -> None:
        if self.validate() is False:
            return

        self._ssd_driver.write(self._address, self._value)

    def validate(self) -> bool:
        if len(self._arguments) != 2:
            return False

        self._address, self._value = self._arguments

        if not isinstance(self._address, int) or not 0 <= self._address <= 99:
            return False

        for v in self._value.strip('0x'):
            if not 'A' <= v <= 'F' and not '0' <= v <= '9':
                return False

        return True
