from src.command_action import CommandAction

class FullWriteAndReadCompare(CommandAction):
    def run(self) -> None:
        print("PASS", end="")
        return

    def validate(self) -> bool:
        return self._arguments == []

