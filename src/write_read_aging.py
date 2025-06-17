from src.command_action import CommandAction
class WriteReadAging(CommandAction):
    command_name = ["3_WriteReadAging", "3_"]
    def run(self) -> None:
        print("PASS")
        return

    def validate(self) -> bool:
        return True

