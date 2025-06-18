from src.commands.command_action import CommandAction, InvalidArgumentException
import sys

class ExitCommand(CommandAction):
    command_name: str = 'exit'
    _description = 'Exit the shell.'
    _usage = 'exit'
    _author = 'Songju Na'
    _alias: list[str] = ['quit', 'q']

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
