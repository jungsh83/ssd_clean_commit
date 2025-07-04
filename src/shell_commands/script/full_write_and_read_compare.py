import random

from src.decorators import log_call
from src.logger import LoggerSingleton, LogLevel
from src.shell_commands.data_dict import PASS_TEXT, FAIL_TEXT
from src.shell_commands.shell_command import ShellCommand, InvalidArgumentException

logger = LoggerSingleton.get_logger()


class FullWriteAndReadCompareShellCommand(ShellCommand):
    command_name: str = "1_FullWriteAndReadCompare"
    _description = 'Execute test scenario: Full Write & Read Compare'
    _usage = "'1_FullWriteAndReadCompare' or '1_'"
    _author = 'Woosung Ji'
    _alias = ['1_']

    def validate(self) -> bool:
        return self._arguments == ()

    @log_call(level=LogLevel.INFO)
    def execute(self) -> str:

        if not self.validate():
            raise InvalidArgumentException(f"{self.command_name} takes no arguments, but got '{self._arguments}'")

        for i in range(25):
            if not self.run_test_case(start_lba=i * 4, test_value=self.generate_test_value()):
                return FAIL_TEXT

        return PASS_TEXT

    def run_test_case(self, start_lba, test_value) -> bool:
        for lba in range(start_lba, start_lba + 4):
            self._ssd_driver.write(lba, test_value)
            if not self.read_compare(lba, test_value):
                return False

        return True

    @staticmethod
    def generate_test_value():
        return f"0x{random.randint(1111111, 4444444):08X}"

    def read_compare(self, lba, test_value) -> bool:
        real_value = self._ssd_driver.read(lba)
        if real_value == test_value:
            return True
        else:
            msg = f"Detected Error Value, lba:{lba}, expected_value:{test_value}, real_value:{real_value}"
            logger.error(msg)
            return False
