import random
from src.logger import LoggerSingleton
from src.decorators import log_call
from src.shell_commands.shell_command import ShellCommand, InvalidArgumentException
from src.data_dict import LBA_START_INDEX, LBA_COUNT

from ..data_dict import *

logger = LoggerSingleton.get_logger()


class WriteReadAgingShellCommand(ShellCommand):
    command_name: str = "3_WriteReadAging"
    _description = 'Execute test scenario: Write Read Aging'
    _usage = "'3_WriteReadAging' or '3_'"
    _author = 'Woosung Ji'
    _alias = ['3_']

    def validate(self) -> bool:
        return self._arguments == ()

    @log_call(level="INFO")
    def execute(self) -> str:
        if not self.validate():
            msg = f"{self.command_name} takes no arguments, but got '{self._arguments}'"
            raise InvalidArgumentException(msg)

        if self._is_test_loop_failed(LBA_START_INDEX):
            return "FAIL"

        elif self._is_test_loop_failed(LBA_COUNT - 1):
            return "FAIL"

        return "PASS"

    def _is_test_loop_failed(self, lba) -> bool:
        for _ in range(200):
            if self._write_read_compare_failed(lba):
                return True
        return False

    def _write_read_compare_failed(self, lba) -> bool:
        test_value = f"0x{self.generate_random_value() :08X}"
        self._ssd_driver.write(lba, test_value)
        read_value = self._ssd_driver.read(lba)

        if read_value != test_value:
            msg = f"Detected Error Value, lba:{lba}, test_value:{test_value}, read_value:{read_value}"
            logger.error(msg)
            return True
        else:
            return False

    def generate_random_value(self):
        return random.randint(1111111, 4444444)
