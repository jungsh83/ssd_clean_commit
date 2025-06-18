from src.commands.command_action import CommandAction, InvalidArgumentException
from src.ssd import VirtualSSD


class FullReadCommand(CommandAction):
    command_name: str = 'fullread'
    _description = 'read value all of LBAs'
    _usage = 'fullread'
    _author = 'Gunam Kwon'
    _alias = []

    VALID_ARGUMENT_LEN = 0

    def __init__(self, ssd_driver, *args: str) -> None:
        super().__init__(ssd_driver, *args)

    def validate(self) -> bool:
        return not self._arguments

    def _dump_all(self) -> list[str]:
        return [
            f"{lba} {self._ssd_driver.read(lba)}"
            for lba in range(VirtualSSD.LBA_COUNT)
        ]

    def run(self) -> str:
        if not self.validate():
            raise InvalidArgumentException(self.get_exception_string())

        return "\n           ".join(self._dump_all())

    def get_exception_string(self):
        return f"{self.command_name} takes {self.VALID_ARGUMENT_LEN} arguments, but got {self._arguments}."
