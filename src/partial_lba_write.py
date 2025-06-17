import random

from src.command_action import CommandAction

WRITE_TEST_VALUE = "0xABCDFFFF"

PARTIAL_LBA_WRITE_COMMAND = ['2_PartialLBAWrite', '2_']


class PartialLBAWrite(CommandAction):
    command_name = PARTIAL_LBA_WRITE_COMMAND

    def run(self) -> None:
        for i in range(30):
            self.bulk_write()

    def bulk_write(self):
        write_order = self.generate_order()

        for lba in write_order:
            self._ssd_driver.write(lba, WRITE_TEST_VALUE)

    def generate_order(self) -> list[int]:
        return [random.randint(0, 5) for _ in range(5)]

    def validate(self) -> bool:
        return True
