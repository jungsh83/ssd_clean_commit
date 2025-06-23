import random
from src.logger import LoggerSingleton
from src.decorators import log_call
from src.shell_commands.shell_command_action import ShellCommandAction, InvalidArgumentException

logger = LoggerSingleton.get_logger()
START_TEST_VALUE = 10000000


class PartialLBAWriteShellCommand(ShellCommandAction):
    command_name: str = "2_PartialLBAWrite"
    _description = 'Execute test scenario: Partial LBA Write'
    _usage = "'2_PartialLBAWrite' or '2_'"
    _author = 'Songhwa Jeong'
    _alias = ['2_']

    def __init__(self, ssd_driver, *args):
        super().__init__(ssd_driver, *args)
        self.test_value = START_TEST_VALUE

    @log_call(level="INFO")
    def run(self) -> str:
        if not self.validate():
            msg = f"{self.command_name} takes no arguments, but got '{self._arguments}'"
            raise InvalidArgumentException(msg)
        for i in range(30):
            self._bulk_write()
            if self._is_read_compare_failed():
                return "FAIL"
        return "PASS"

    def _is_read_compare_failed(self):
        for read_lba in range(5):
            test_value = self._get_test_value()
            real_value = self._ssd_driver.read(read_lba)

            if test_value != real_value:
                msg = f"Detected Error Value, lba:{read_lba}, test_value:{test_value}, real_value:{real_value}"
                logger.error(msg)
                return True

        return False

    def _bulk_write(self):
        self.test_value += 1

        for lba in self._generate_order():
            self._ssd_driver.write(lba, self._get_test_value())

    def _get_test_value(self):
        return f'0x{self.test_value}'

    def _generate_order(self) -> list[int]:
        orders = list(range(5))  # [0, 1, 2, 3, 4]
        random.shuffle(orders)

        return orders

    def validate(self) -> bool:
        return self._arguments == ()
