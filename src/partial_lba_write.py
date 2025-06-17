from src.command_action import CommandAction

PARTIAL_LBA_WRITE_COMMAND = ['2_PartialLBAWrite', '2_']


class PartialLBAWrite(CommandAction):
    command_name = PARTIAL_LBA_WRITE_COMMAND

    def run(self) -> None:
        pass

    def validate(self) -> bool:
        return True
