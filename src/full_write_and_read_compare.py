import random
from src.command_action import CommandAction


class FullWriteAndReadCompare(CommandAction):
    command_name = ["1_FullWriteAndReadCompare", "1_"]

    def validate(self) -> bool:
        return self._arguments == []

    def run(self) -> None:
        for i in range(25):
            if not self.run_test_case(start_lba=i * 4, test_value=self.generate_test_value()):
                print("FAIL")
                return

        print("PASS")
        return

    def run_test_case(self, start_lba, test_value) -> bool:
        for lba in range(start_lba, start_lba + 4):
            self._ssd_driver.write(lba, test_value)
            if not self.read_compare(lba, test_value):
                return False

        return True

    def generate_test_value(self):
        return f"0x{random.randint(1111111, 4444444):08X}"

    def read_compare(self, lba, test_value) -> bool:
        return self._ssd_driver.read(lba) == test_value
