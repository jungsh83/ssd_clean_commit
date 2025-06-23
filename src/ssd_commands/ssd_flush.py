from src.command_buffer_handler import CommandBufferHandler
from src.ssd_commands.ssd_command_action import SSDCommand
from src.ssd_file_manager import SSDFileManager


class SSDFlushCommand(SSDCommand):
    def __init__(self, ssd_file_manager: SSDFileManager, command_buffer: CommandBufferHandler, *args):
        super().__init__(ssd_file_manager, command_buffer, *args)

    def run(self) -> str:
        cmd_buffers = self._command_buffer.read_all()

        for cmd in cmd_buffers:
            if cmd.command_type == "W":
                self._ssd_file_manager.write(cmd.lba, cmd.value)
            elif cmd.command_type == "E":
                self._ssd_file_manager.erase(cmd.lba, cmd.value)

        self._command_buffer.initialize()

    def validate(self) -> bool:
        return self._arguments == ()
