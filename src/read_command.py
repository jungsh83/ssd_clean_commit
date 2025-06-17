from src.command_action import CommandAction


class ReadCommand(CommandAction):
    command_name: list = ['read']

    def __init__(self, ssd_driver, *args):
        super().__init__(ssd_driver, *args)
        self._address: int = self._arguments

    def run(self) -> str:
        return self._ssd_driver.read(self._address)

    def validate(self) -> bool:
        pass
