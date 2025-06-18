from __future__ import annotations
from typing import List
from src.command_action import CommandAction


class FullRead(CommandAction):
    command_name = ["fullread", "fr"]
    ERROR_UNVALIDATED = "Validation Error"

    def __init__(self, ssd_driver, *arguments: str) -> None:
        super().__init__(ssd_driver, *arguments)

    def validate(self) -> bool:
        return not self._arguments

    def _dump_all(self) -> List[str]:
        return [
            self._ssd_driver.read(lba)
            for lba in range(self._ssd_driver.LBA_COUNT)
        ]

    def run(self) -> None:
        if not self.validate():
            raise ValueError(self.ERROR_UNVALIDATED)

        for value in self._dump_all():
            print(value)
