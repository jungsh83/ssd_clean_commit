import random
from src.shell_commands.shell_command_action import ShellCommandAction, InvalidArgumentException

DEFAULT_METHOD = "0x00000000"


class EraseAndWriteAging(ShellCommandAction):
    command_name: str = "4_EraseAndWriteAging"
    _description = 'Execute test scenario: Erase and Write Aging'
    _usage = "'4_EraseAndWriteAging' or '4_'"
    _author = 'Woosung Ji'
    _alias = ['4_']

    def validate(self) -> bool:
        return self._arguments == ()

    def run(self) -> str:

        if not self.validate():
            msg = f"{self.command_name} takes no arguments, but got '{self._arguments}'"
            raise InvalidArgumentException(msg)

        self._ssd_driver.erase(0, 2)

        for _ in range(30):
            for start_lba in range(2, 100, 2):
                if not self.run_single_test(start_lba):
                    return "FAIL"

        return "PASS"

    def run_single_test(self, start_lba) -> bool:
        self._ssd_driver.write(start_lba, self.generate_test_value())
        self._ssd_driver.write(start_lba, self.generate_test_value())
        self._ssd_driver.erase(start_lba, 3)

        for lba in range(start_lba, start_lba + 3):
            if not self.read_compare(lba, DEFAULT_METHOD):
                return False

        return True

    def generate_test_value(self):
        return f"0x{random.randint(1111111, 4444444):08X}"

    def read_compare(self, lba, test_value) -> bool:
        return self._ssd_driver.read(lba) == test_value
