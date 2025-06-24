from src.command_buffer.command_buffer_data import CommandBufferData, WRITE, ERASE
from src.command_buffer.command_buffer_handler import CommandBufferHandler
from src.data_dict import INIT_VAL_INT, INIT_VAL_STR
from src.ssd_commands import validate_lba, validate_value
from src.ssd_commands.ssd_command import SSDCommand
from src.ssd_file_manager import SSDFileManager


class WriteSSDCommand(SSDCommand):
    def __init__(self, ssd_file_manager: SSDFileManager, command_buffer: CommandBufferHandler, *args):
        super().__init__(ssd_file_manager, command_buffer, *args)

        self.lba: int = INIT_VAL_INT
        self.value: str = INIT_VAL_STR

    def execute(self) -> str:
        if not self.validate():
            self._ssd_file_manager.error()
            return "FAIL"

        # Buffer가 가득차 있다면 flush 수행
        if not self._command_buffer.is_buffer_available():
            self.do_flush()

        # Command를 buffer에 추가
        self.append_command_into_command_buffer()

        return "PASS"

    def append_command_into_command_buffer(self):
        self._command_buffer.append(
            CommandBufferData.create_write_command(lba=self.lba, value=self.value)
        )

    def validate(self) -> bool:
        if len(self._arguments) != 2:
            return False

        self.lba = int(self._arguments[0])
        self.value = self._arguments[1]

        if not validate_lba(self.lba):
            return False

        if not validate_value(self.value):
            return False

        return True

    def do_flush(self):
        # command들을 fileManager를 통해 수행
        for command in self._command_buffer.command_buffers:
            if command.command_type == WRITE:
                self._ssd_file_manager.write(command.lba, command.value)
            elif command.command_type == ERASE:
                self._ssd_file_manager.erase(command.lba, command.size)

        # command buffer를 초기화
        self._command_buffer.initialize()

        return
