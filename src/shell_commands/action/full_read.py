from src.shell_commands.shell_command_action import ShellCommandAction, InvalidArgumentException
from src.ssd_file_manager import SSDFileManager
from ..data_dict import *


class FullReadShellCommand(ShellCommandAction):
    command_name: str = 'fullread'
    _description = 'read value all of LBAs'
    _usage = 'fullread'
    _author = 'Gunam Kwon'
    _alias = []

    def __init__(self, ssd_driver, *arguments: str) -> None:
        super().__init__(ssd_driver, *arguments)

    def validate(self) -> bool:
        return self._arguments == ()

    def _dump_all(self) -> list[str]:
        return [
            f"{lba} {self._ssd_driver.read(lba)}"
            for lba in range(LBA_COUNT)
        ]

    def run(self) -> str:
        if not self.validate():
            raise InvalidArgumentException(self.get_exception_string())

        return "\n           ".join(self._dump_all())

    def get_exception_string(self):
        return f"{self.command_name} takes no arguments, but got {self._arguments}."
