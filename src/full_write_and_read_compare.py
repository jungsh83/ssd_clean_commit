from src.command_action import CommandAction

class FullWriteAndReadCompare(CommandAction):
    def run(self) -> None:

        for i in range(25):
            test_value = "0x12345678"
            for addr in range(i*4, i*4+4):
                self._ssd_driver.write(addr, test_value)
                if not self.read_compare(addr, test_value):
                    print("FAIL", end="")
                    return

        print("PASS", end="")
        return

    def validate(self) -> bool:
        return self._arguments == []

    def read_compare(self, addr, test_value) -> bool:
        return self._ssd_driver.read(addr) == test_value


