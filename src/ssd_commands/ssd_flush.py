from src.command_buffer.command_buffer_handler import CommandBufferHandler

from src.command_buffer.command_buffer_data import WRITE, ERASE
from src.ssd_commands.ssd_command import SSDCommand
from src.ssd_file_manager import SSDFileManager


class FlushSSDCommand(SSDCommand):
    def __init__(self, ssd_file_manager: SSDFileManager, command_buffer: CommandBufferHandler, *args):
        super().__init__(ssd_file_manager, command_buffer, *args)

    def execute(self) -> str:
        if not self.validate():
            self._ssd_file_manager.error()
            return "FAIL"

        for cmd in self._command_buffer.command_buffers:
            if cmd.command_type == WRITE:
                self._ssd_file_manager.write(cmd.lba, cmd.value)
            elif cmd.command_type == ERASE:
                self._ssd_file_manager.erase(cmd.lba, cmd.value)

        self._command_buffer.initialize()

        return "PASS"

    def validate(self) -> bool:
        return self._arguments == ()