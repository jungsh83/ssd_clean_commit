import random
from src.shell_commands.command_action import CommandAction, InvalidArgumentException
from src.ssd_file_manager import SSDFileManager

class WriteReadAgingCommand(CommandAction):
    command_name: str = "3_WriteReadAging"
    _description = 'Execute test scenario: Write Read Aging'
    _usage = "'3_WriteReadAging' or '3_'"
    _author = 'Woosung Ji'
    _alias = ['3_']

    def validate(self) -> bool:
        return self._arguments == ()

    def run(self) -> str:
        if not self.validate():
            msg = f"{self.command_name} takes no arguments, but got '{self._arguments}'"
            raise InvalidArgumentException(msg)

        if self._test_loop_failed(SSDFileManager.LBA_START_INDEX):
            return "FAIL"

        elif self._test_loop_failed(SSDFileManager.LBA_COUNT - 1):
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
