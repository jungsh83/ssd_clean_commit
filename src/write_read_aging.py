from src.command_action import CommandAction
class WriteReadAging(CommandAction):
    command_name = ["3_WriteReadAging", "3_"]

    def validate(self) -> bool:
        return self._arguments == []

    def run(self) -> None:
        print("PASS")
        return



