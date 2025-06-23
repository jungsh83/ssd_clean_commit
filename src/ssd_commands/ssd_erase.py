from src.ssd_commands import validate_erase_size, validate_lba
from src.ssd_commands.ssd_command_action import SSDCommand
from src.ssd_file_manager import SSDFileManager
from src.command_buffer.command_buffer_handler import CommandBufferHandler
from src.command_buffer.command_buffer_data import CommandBufferData, WRITE, ERASE


class SSDWriteCommand(SSDCommand):
    def __init__(self, ssd_file_manager: SSDFileManager, command_buffer: CommandBufferHandler, *args):
        super().__init__(ssd_file_manager, command_buffer, *args)
        self.lba = -1
        self.size = -1

    def validate(self) -> bool:
        if len(self._arguments) != 2:
            return False

        lba_str, size_str = self._arguments

        return (
                validate_lba(lba_str) and
                validate_erase_size(size_str)
        )

    def run(self) -> str:
        if not self.validate():
            self._ssd_file_manager.error()
            return "FAIL"

        self.lba, self.size = self._arguments[0], self._arguments[1]

        if not self._command_buffer.is_buffer_available():
            self.do_flush()

        # Command를 buffer에 추가
        self.append_command_into_command_buffer()

        return "PASS"

    def append_command_into_command_buffer(self):
        self._command_buffer.append(
            CommandBufferData.create_erase_command(lba=self.lba, size=self.size)
        )

    def do_flush(self):
        """
        :return:
        """

        # command들을 fileManager를 통해 수행
        for command in self._command_buffer.command_buffers:
            if command.command_type == WRITE:
                self._ssd_file_manager.write(command.lba, command.value)
            elif command.command_type == ERASE:
                self._ssd_file_manager.erase(command.lba, command.size)

            # command buffer를 초기화
        self._command_buffer.initialize()

        return
