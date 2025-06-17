import random
from src.command_action import CommandAction

TEST_ADDRESS_1 = 0
TEST_ADDRESS_2 = 99


class WriteReadAging(CommandAction):
    command_name = ["3_WriteReadAging", "3_"]

    def validate(self) -> bool:
        return self._arguments == []

    def run(self) -> None:
        for _ in range(200):
            self.write_data()
            if not self.read_compare(TEST_ADDRESS_1, TEST_ADDRESS_2):
                print("FAIL")
                return

        print("PASS")
        return

    def write_data(self):
        test_value = f"0x{random.randint(1111111, 4444444):08X}"
        self._ssd_driver.write(TEST_ADDRESS_1, test_value)
        self._ssd_driver.write(TEST_ADDRESS_2, test_value)

    def read_compare(self, addr1, addr2) -> bool:
        return self._ssd_driver.read(addr1) == self._ssd_driver.read(addr2)
