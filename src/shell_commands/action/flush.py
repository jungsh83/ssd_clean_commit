from src.decorators import log_call
from src.shell_commands.shell_command import ShellCommand, InvalidArgumentException


class FlushShellCommand(ShellCommand):
    command_name: str = 'flush'
    _description = 'flush buffers'
    _usage = 'flush buffers'
    _author = 'Gunam Kwon'
    _alias = ['f']

    @log_call(level="INFO")
    def __init__(self, ssd_driver, *arguments: str) -> None:
        super().__init__(ssd_driver, *arguments)

    def validate(self) -> bool:
        return self._arguments == ()

    @log_call(level="INFO")
    def execute(self) -> str:
        if not self.validate():
            raise InvalidArgumentException(self.get_exception_string())

        self._ssd_driver.flush()
        return "Done"

    def get_exception_string(self):
        return f"{self.command_name} takes no arguments, but got {self._arguments}."
