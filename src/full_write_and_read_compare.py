import random
from src.command_action import CommandAction


class FullWriteAndReadCompare(CommandAction):
    def run(self) -> None:
        for i in range(25):
            if not self.run_test_case(start_addr=i * 4, test_value=self.generate_test_value()):
                print("FAIL")
                return

        print("PASS", end="")
        return

    def run_test_case(self, start_addr, test_value) -> bool:
        for addr in range(start_addr, start_addr + 4):
            self._ssd_driver.write(addr, test_value)
            if not self.read_compare(addr, test_value):
                return False

        return True

    def generate_test_value(self):
        return f"0x{random.randint(1111111, 4444444):08X}"

    def validate(self) -> bool:
        return self._arguments == []

    def read_compare(self, addr, test_value) -> bool:
        return self._ssd_driver.read(addr) == test_value
