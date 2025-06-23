from src.ssd_commands.ssd_command_action import SSDCommand, InvalidArgumentException
from src.ssd_commands import validate_lba, validate_value


class ReadCommand(SSDCommand):
    command_name = ['read', 'r']

    def __init__(self, ssd_file_manager, command_buffer, *args):
        super().__init__(ssd_file_manager, command_buffer, *args)
        self._lba = None

    def validate(self) -> bool:
        if len(self._arguments) != 1:
            return False
        if not validate_lba(self._arguments[0]):
            return False

        self._lba = int(self._arguments[0])
        return True

    def run(self) -> None:
        if not self.validate():
            self._ssd_file_manager.error()
            return

        buffered_value = self._command_buffer.fast_read(self._lba)

        if buffered_value is not None:
            self._ssd_file_manager.write_output(buffered_value)
            return

        self._ssd_file_manager.read(self._lba)
