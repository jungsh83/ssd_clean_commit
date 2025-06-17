from src.command_action import CommandAction

PARTIAL_LBA_WRITE_COMMAND = ['2_PartialLBAWrite', '2_']


class PartialLBAWrite(CommandAction):
    command_name = PARTIAL_LBA_WRITE_COMMAND

    def run(self) -> None:
        for i in range(30):
            self._ssd_driver.write(4, "0xABCDFFFF")
            self._ssd_driver.write(0, "0xABCDFFFF")
            self._ssd_driver.write(3, "0xABCDFFFF")
            self._ssd_driver.write(1, "0xABCDFFFF")
            self._ssd_driver.write(2, "0xABCDFFFF")


    def validate(self) -> bool:
        return True
