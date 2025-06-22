import os
from pathlib import Path

from src.command_buffer_data import ERASE_VALUE, ERASE, WRITE, EMPTY, CommandBufferDataException, CommandBufferData
from src.command_buffer_file_manager import CommandBufferFileManager
from src.command_buffer_optimizer import CommandBufferOptimizer, IgnoreCommandStrategy, MergeEraseStrategy, \
    CommandBufferOptimizeStrategy


class CommandBufferHandlerException(Exception):
    pass


class CommandBufferHandler:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    COMMAND_BUFFER_DIR_PATH = Path(os.path.join(BASE_DIR, 'buffer'))

    def __init__(self):
        self._file_manager = CommandBufferFileManager()
        self._command_buffers = self.read_all()

    @property
    def command_buffers(self):
        return self._command_buffers

    def fast_read(self, lba: int) -> str | None:
        for command in reversed(self._command_buffers):
            if command.command_type == EMPTY:
                continue
            if command.start_lba <= lba < command.end_lba:
                return command.value
        return None

    def is_empty_buffer_slot_existing(self) -> bool:
        for command in self._command_buffers:
            if command.command_type == EMPTY:
                return True
        return False

    def _append_command(self, new_command):
        if not self.is_empty_buffer_slot_existing():
            raise CommandBufferHandlerException("남아 있는 Buffer Slot이 없습니다.")

        for command in self._command_buffers:
            if command.command_type == EMPTY:
                command.command_type = new_command.command_type
                command.lba = new_command.lba
                command.value = new_command.value
                command.size = new_command.size
                break

    def append(self, new_command: CommandBufferData):
        self._append_command(new_command)
        self._optimize(IgnoreCommandStrategy())
        self._optimize(MergeEraseStrategy())
        self._file_manager.update_command_buffers_to_file_name(self._command_buffers)

    def _optimize(self, strategy: CommandBufferOptimizeStrategy):
        optimizer = CommandBufferOptimizer(strategy)
        self._command_buffers = optimizer.optimize(self._command_buffers)

    def read_all(self):
        if self._file_manager.is_not_initialized():
            self.initialize()

        result = self._file_manager.read_command_buffers_from_file_name()

        result.sort(key=lambda cmd: cmd.order)
        return result

    def initialize(self):
        self._command_buffers = [CommandBufferData(order=order) for order in range (1, 6)]

        if self._file_manager.is_not_initialized():
            self._file_manager.initialize_file(self._command_buffers)

        self._file_manager.update_command_buffers_to_file_name(self.command_buffers)
