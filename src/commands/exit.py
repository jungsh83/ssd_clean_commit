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
            raise InvalidArgumentException(f"{self.__class__.command_name} takes 0 arguments, but got {self._arguments}")
        print("[EXIT]")
        # sys.exit(0)
        return

    def validate(self) -> bool:
        return len(self._arguments) == 0
