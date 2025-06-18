import random

from src.command_action import CommandAction

WRITE_TEST_VALUE = "0xABCDFFFF"

PARTIAL_LBA_WRITE_COMMAND = ['2_PartialLBAWrite', '2_']


class PartialLBAWrite(CommandAction):
    command_name = PARTIAL_LBA_WRITE_COMMAND

    def __init__(self, ssd_driver, *args):
        super().__init__(ssd_driver, *args)
        self.test_value = 10000000

    def run(self) -> str:
        for i in range(30):
            self.bulk_write()
            if self.is_read_compare_failed():
                return "FAIL"
        return "PASS"

    def is_read_compare_failed(self):
        for read_lba in range(5):
            if not self.get_test_value() == self._ssd_driver.read(read_lba):
                return True
        return False

    def bulk_write(self):
        write_order = self.generate_order()

        self.test_value += 1

        for lba in write_order:
            self._ssd_driver.write(lba, self.get_test_value())

    def get_test_value(self):
        return f'0x{self.test_value}'

    def generate_order(self) -> list[int]:
        orders = list(range(5))  # [0, 1, 2, 3, 4]
        random.shuffle(orders)

        return orders

    def validate(self) -> bool:
        if self._arguments:
            return False
        return True
