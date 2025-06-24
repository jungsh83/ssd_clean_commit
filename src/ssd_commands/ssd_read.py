from src.data_dict import VALID_ARGUMENT_SINGLE, INIT_VAL_INT
from src.ssd_commands import validate_lba
from src.ssd_commands.ssd_command import SSDCommand


class ReadSSDCommand(SSDCommand):
    command_name = ['read', 'r']

    def __init__(self, ssd_file_manager, command_buffer, *args):
        super().__init__(ssd_file_manager, command_buffer, *args)
        self._lba = INIT_VAL_INT

    def validate(self) -> bool:

        if len(self._arguments) != VALID_ARGUMENT_SINGLE:
            return False
        if not validate_lba(self._arguments[0]):
            return False

        self._lba = int(self._arguments[0])
        return True

    def execute(self) -> None:
        if not self.validate():
            self._ssd_file_manager.error()
            return

        buffered_value = self._command_buffer.fast_read(self._lba)

        if buffered_value is not None:
            self._ssd_file_manager.write_output(buffered_value)
            return

        self._ssd_file_manager.read(self._lba)
