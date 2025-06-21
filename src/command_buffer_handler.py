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
        for command in reversed(self.command_buffers):
            if command.command_type == EMPTY:
                continue
            if command.start_lba <= lba < command.end_lba:
                return command.value
        return None

    def is_empty_buffer_slot_existing(self) -> bool:
        for command in self.command_buffers:
            if command.command_type == EMPTY:
                return True
        return False

    def _append_command(self, new_command):
        insert_order = 0
        for command in self.command_buffers:
            if command.command_type == EMPTY:
                new_command.order = command.order
                break
            else:
                insert_order += 1

        if insert_order >= 5:
            raise CommandBufferHandlerException("남아 있는 Buffer Slot이 없습니다.")

        new_command.order = insert_order + 1
        self._command_buffers[insert_order] = new_command

    def append(self, command: CommandBufferData):
        try:
            new_command = command
            if command.command_type == WRITE and command.value == ERASE_VALUE:
                new_command = CommandBufferData.create_erase_command(lba=command.lba, size=1)

            self._append_command(new_command)
            self._optimize(IgnoreCommandStrategy())
            self._optimize(MergeEraseStrategy())
            self._file_manager.update_command_buffers_to_file_name(self.command_buffers)
        except CommandBufferDataException as e:
            raise e
        except Exception:
            raise CommandBufferHandlerException("Buffer 처리 실패하였습니다.")

    def _optimize(self, strategy: CommandBufferOptimizeStrategy):
        optimizer = CommandBufferOptimizer(strategy)
        self._command_buffers = optimizer.optimize(self.command_buffers)

    def read_all(self):
        if self._file_manager.is_not_initialized():
            self.initialize()

        result = self._file_manager.read_command_buffers_from_file_name()

        result.sort(key=lambda cmd: cmd.order)
        return result

    def initialize(self):
        self._command_buffers = [
            CommandBufferData(order=1),
            CommandBufferData(order=2),
            CommandBufferData(order=3),
            CommandBufferData(order=4),
            CommandBufferData(order=5)
        ]
        self._file_manager.initialize_file_name(self.command_buffers)
