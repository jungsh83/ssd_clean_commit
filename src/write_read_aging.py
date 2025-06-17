import random
from src.command_action import CommandAction


class WriteReadAging(CommandAction):
    command_name = ["3_WriteReadAging", "3_"]

    def validate(self) -> bool:
        return self._arguments == []

    def run(self) -> None:
        for _ in range(200):
            test_value = self.generate_test_value()
            self._ssd_driver.write(0, test_value)
            self._ssd_driver.write(99, test_value)

            if self._ssd_driver.read(0) == self._ssd_driver.read(99):
                pass
            else:
                print("FAIL")
                return

        print("PASS")
        return

    def generate_test_value(self):
        return f"0x{random.randint(1111111, 4444444):08X}"