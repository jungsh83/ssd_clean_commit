import random

from src.command_action import CommandAction

WRITE_TEST_VALUE = "0xABCDFFFF"

PARTIAL_LBA_WRITE_COMMAND = ['2_PartialLBAWrite', '2_']


class PartialLBAWrite(CommandAction):
    command_name = PARTIAL_LBA_WRITE_COMMAND

    def run(self) -> str:
        for i in range(30):
            self.bulk_write()
            for read_lba in range(5):
                if not WRITE_TEST_VALUE == self._ssd_driver.read(read_lba):
                    return "FAIL"
        return "PASS"

    def bulk_write(self):
        write_order = self.generate_order()

        for lba in write_order:
            self._ssd_driver.write(lba, WRITE_TEST_VALUE)

    def generate_order(self) -> list[int]:
        orders = list(range(5))  # [0, 1, 2, 3, 4]
        random.shuffle(orders)

        return orders

    def validate(self) -> bool:
        if self._arguments:
            return False
        return True
