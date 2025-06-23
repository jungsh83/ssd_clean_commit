from src.shell_commands.shell_command_action import ShellCommandAction, InvalidArgumentException
from src.decorators import log_call


class ExitShellCommand(ShellCommandAction):
    command_name: str = 'exit'
    _description = 'Exit the shell.'
    _usage = 'exit'
    _author = 'Songju Na'
    _alias: list[str] = ['quit', 'q']

    @log_call(level="INFO")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @log_call(level="INFO")
    def run(self):
        if not self.validate():
            raise InvalidArgumentException(self.get_exception_string())
        print("[EXIT]")
        # sys.exit(0)
        return

    def validate(self) -> bool:
        return self._arguments == ()

    def get_exception_string(self):
        return f"{self.command_name} takes no arguments, but got {self._arguments}."
