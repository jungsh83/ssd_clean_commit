# src/exit_command.py
from src.command_action import CommandAction
import sys

class ExitCommand(CommandAction):
    command_name: str = 'exit'
    _description = 'Exit the shell.'
    _usage = 'exit'
    _author = 'Songju Na'
    _alias: list[str] = ['quit', 'q']

    def run(self):
        if not self.validate():
            raise Exception(f"exit command takes no arguments, but got {self._arguments}")
        print("[EXIT]")
        sys.exit(0)

    def validate(self) -> bool:
        return len(self._arguments) == 0
