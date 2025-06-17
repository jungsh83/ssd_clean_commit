import random
from src.command_action import CommandAction

TEST_LBA_1 = 0
TEST_LBA_2 = 99


class WriteReadAging(CommandAction):
    command_name = ["3_WriteReadAging", "3_"]

    def validate(self) -> bool:
        return self._arguments == []

    def run(self) -> None:
        for _ in range(200):
            self.write_data()
            if not self.read_compare(TEST_LBA_1, TEST_LBA_2):
                print("FAIL")
                return

        print("PASS")
        return

    def write_data(self):
        test_value = f"0x{random.randint(1111111, 4444444):08X}"
        self._ssd_driver.write(TEST_LBA_1, test_value)
        self._ssd_driver.write(TEST_LBA_2, test_value)

    def read_compare(self, lba1, lba2) -> bool:
        return self._ssd_driver.read(lba1) == self._ssd_driver.read(lba2)
