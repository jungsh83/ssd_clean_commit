from src.commands.command_action import CommandAction


class ReadCommand(CommandAction):
    ERROR_UNVALIDATED = 'Validation Error'
    command_name: str = 'read'

    def __init__(self, ssd_driver, *args):
        super().__init__(ssd_driver, *args)
        self._address = None

    def run(self) -> str:
        if self.validate() is False:
            raise ValueError(self.ERROR_UNVALIDATED)

        return f'LBA {self._address} : {self._ssd_driver.read(self._address)}'

    def validate(self) -> bool:
        if len(self._arguments) != 1:
            return False

        self._address: int = self._arguments[0]
        if not isinstance(self._address, int) or (not 0 <= self._address <= 99):
            return False

        return True
