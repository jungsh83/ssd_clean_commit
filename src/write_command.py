from src.command_action import CommandAction


class WriteCommand(CommandAction):
    def __init__(self, ssd_driver, *args):
        super().__init__(ssd_driver, *args)
        self._address, self._value = self._arguments

    def run(self) -> None:
        if self.validate() is False:
            return
        self._ssd_driver.write(self._address, self._value)

    def validate(self) -> bool:
        if self._address == 200 or self._address == -1:
            return False
        else:
            return True
