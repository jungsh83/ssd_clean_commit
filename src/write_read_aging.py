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
            if self._write_read_compare_failed(TEST_LBA_1):
                return "FAIL"
            if self._write_read_compare_failed(TEST_LBA_2):
                return "FAIL"

        return "PASS"

    def _write_read_compare_failed(self, lba) -> bool:
        test_value = f"0x{random.randint(1111111, 4444444):08X}"
        self._ssd_driver.write(lba, test_value)
        read_value = self._ssd_driver.read(lba)

        return read_value != test_value
