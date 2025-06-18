from src.command_action import CommandAction


class FullWriteCommand(CommandAction):
    command_name = ['fullwrite']

    def __init__(self, ssd_driver, *args):
        super().__init__(ssd_driver, *args)
        self._value = self._arguments[0]

    def run(self) -> None:
        if self.validate() is False:
            raise ValueError()

        for address in range(100):
            self._ssd_driver.write(address, self._value)

    def validate(self) -> bool:
        if not isinstance( self._value, str):
            return False

        return True
