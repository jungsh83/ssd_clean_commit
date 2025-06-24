from src.decorators import log_call
from src.shell_commands.shell_command import ShellCommand, InvalidArgumentException
from src.shell_commands.data_dict import LBA_COUNT
from src.logger import LogLevel


class FullReadShellCommand(ShellCommand):
    command_name: str = 'fullread'
    _description = 'read value all of LBAs'
    _usage = 'fullread'
    _author = 'Gunam Kwon'
    _alias = []

    @log_call(level=LogLevel.INFO)
    def __init__(self, ssd_driver, *arguments: str) -> None:
        super().__init__(ssd_driver, *arguments)

    def validate(self) -> bool:
        return self._arguments == ()

    def _dump_all(self) -> list[str]:
        return [
            f"{lba} {self._ssd_driver.read(lba)}"
            for lba in range(LBA_COUNT)
        ]

    @log_call(level=LogLevel.INFO)
    def execute(self) -> str:
        if not self.validate():
            raise InvalidArgumentException(self.get_exception_string())

        return "\n           ".join(self._dump_all())

    def get_exception_string(self):
        return f"{self.command_name} takes no arguments, but got {self._arguments}."
