import random
from src.logger import LoggerSingleton
from src.decorators import log_call
from src.shell_commands.shell_command_action import ShellCommandAction, InvalidArgumentException

logger = LoggerSingleton.get_logger()


class FullWriteAndReadCompareShellCommand(ShellCommandAction):
    command_name: str = "1_FullWriteAndReadCompare"
    _description = 'Execute test scenario: Full Write & Read Compare'
    _usage = "'1_FullWriteAndReadCompare' or '1_'"
    _author = 'Woosung Ji'
    _alias = ['1_']

    def validate(self) -> bool:
        return self._arguments == ()

    @log_call(level="INFO")
    def run(self) -> str:

        if not self.validate():
            msg = f"{self.command_name} takes no arguments, but got '{self._arguments}'"
            raise InvalidArgumentException(msg)

        for i in range(25):
            if not self.run_test_case(start_lba=i * 4, expected_value=self.generate_test_value()):
                return "FAIL"

        return "PASS"

    def run_test_case(self, start_lba, expected_value) -> bool:
        for lba in range(start_lba, start_lba + 4):
            self._ssd_driver.write(lba, expected_value)
            if not self.read_compare(lba, expected_value):
                return False

        return True

    def generate_test_value(self):
        return f"0x{random.randint(1111111, 4444444):08X}"

    def read_compare(self, lba, expected_value) -> bool:
        return self._ssd_driver.read(lba) == expected_value
