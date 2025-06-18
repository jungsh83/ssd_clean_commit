from src.commands.command_action import CommandAction


class FullReadCommand(CommandAction):
    command_name = ["fullread", "fr"]
    ERROR_UNVALIDATED = "Validation Error"

    def __init__(self, ssd_driver, *arguments: str) -> None:
        super().__init__(ssd_driver, *arguments)

    def validate(self) -> bool:
        return not self._arguments

    def _dump_all(self) -> list[str]:
        return [
            f"{lba} {self._ssd_driver.read(lba)}"
            for lba in range(self._ssd_driver.LBA_COUNT)
        ]

    def run(self) -> str:
        if not self.validate():
            raise ValueError(self.ERROR_UNVALIDATED)

        return "\n           ".join(self._dump_all())
