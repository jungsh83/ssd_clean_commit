from src.command_buffer.command_buffer_data import CommandBufferData, WRITE, ERASE
from src.command_buffer.command_buffer_handler import CommandBufferHandler
from src.data_dict import ERASE_SIZE_MIN, VALID_ARGUMENT_RANGE, INIT_VAL_INT, PASS_TEXT, FAIL_TEXT
from src.ssd_commands import validate_erase_size, validate_lba
from src.ssd_commands.ssd_command import SSDCommand
from src.ssd_file_manager import SSDFileManager


class EraseSSDCommand(SSDCommand):
    def __init__(self, ssd_file_manager: SSDFileManager, command_buffer: CommandBufferHandler, *args):
        super().__init__(ssd_file_manager, command_buffer, *args)
        self.lba = INIT_VAL_INT
        self.size = INIT_VAL_INT

    def validate(self) -> bool:
        if len(self._arguments) != VALID_ARGUMENT_RANGE:
            return False

        lba_str, size_str = self._arguments

        return (
                validate_lba(lba_str) and
                validate_erase_size(size_str)
        )

    def execute(self) -> str:
        if not self.validate():
            self._ssd_file_manager.error()
            return FAIL_TEXT

        self.lba, self.size = int(self._arguments[0]), int(self._arguments[1])

        if self.size == ERASE_SIZE_MIN:
            return PASS_TEXT

        if not self._command_buffer.is_buffer_available():
            self.do_flush()

        # Command를 buffer에 추가
        self.append_command_into_command_buffer()

        return PASS_TEXT

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
