import random
from src.commands.command_action import CommandAction, InvalidArgumentException

TEST_LBA_1 = 0
TEST_LBA_2 = 99


class WriteReadAgingCommand(CommandAction):
    command_name: list[str] = ["3_WriteReadAging"]
    _description = 'Execute test scenario: Write Read Aging'
    _usage = "'3_WriteReadAging' or '3_'"
    _author = 'Woosung Ji'
    _alias = ['3_']

    def validate(self) -> bool:
        return self._arguments == ()

    def run(self) -> str:
        if not self.validate():
            msg = f"{self.command_name[0]} takes no arguments, but got '{self._arguments}'"
            raise InvalidArgumentException(msg)

        if self._test_loop_failed(TEST_LBA_1):
            return "FAIL"

        elif self._test_loop_failed(TEST_LBA_2):
            return "FAIL"

        return "PASS"

    def _test_loop_failed(self, lba) -> bool:
        for _ in range(200):
            if self._write_read_compare_failed(lba):
                return True
        return False

    def _write_read_compare_failed(self, lba) -> bool:
        test_value = f"0x{random.randint(1111111, 4444444):08X}"
        self._ssd_driver.write(lba, test_value)
        read_value = self._ssd_driver.read(lba)

        return read_value != test_value
