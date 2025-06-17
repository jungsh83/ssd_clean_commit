from src.command_action import CommandAction


class PartialLBAWrite(CommandAction):
    command_name = ['2_PartialLBAWrite', '2_']

    def run(self) -> None:
        pass

    def validate(self) -> bool:
        return True
