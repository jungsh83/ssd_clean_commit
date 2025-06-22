from src.command_buffer.command_buffer_data import ERASE_VALUE, ERASE, WRITE, EMPTY, CommandBufferData, \
    MAX_SIZE_OF_COMMAND_BUFFERS
from src.command_buffer.command_buffer_file_manager import CommandBufferFileManager
from src.command_buffer.command_buffer_optimizer import CommandBufferOptimizer, IgnoreCommandStrategy, MergeEraseStrategy, \
    CommandBufferOptimizeStrategy


class CommandBufferHandlerException(Exception):
    pass


class CommandBufferHandler:

    def __init__(self):
        self._file_manager = CommandBufferFileManager()
        self._command_buffers = self.read_all()

    @property
    def command_buffers(self):
        return self._command_buffers

    def initialize(self):
        self._command_buffers = [CommandBufferData(order=index + 1) for index in range(MAX_SIZE_OF_COMMAND_BUFFERS)]
        self._apply_changes()

    def read_all(self):
        result = self._file_manager.read_command_buffers_from_file_name()

        result.sort(key=lambda cmd: cmd.order)
        return result

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

    def append(self, new_command: CommandBufferData):
        new_command = self._transform_command(new_command)
        self._append_command(new_command)
        self._optimize([IgnoreCommandStrategy(), MergeEraseStrategy()])
        self._apply_changes()

    def _transform_command(self, command):
        new_command = command
        if command.command_type == WRITE and command.value == ERASE_VALUE:
            new_command = CommandBufferData(command_type=ERASE, lba=command.lba, size=1)
        return new_command

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

    def _optimize(self, strategies: list[CommandBufferOptimizeStrategy]):
        for strategy in strategies:
            optimizer = CommandBufferOptimizer(strategy)
            self._command_buffers = optimizer.optimize(self._command_buffers)

    def _apply_changes(self):
        self._file_manager.write_command_buffers_to_file_name(self._command_buffers)
