from src.ssd_file_manager import SSDFileManager
from src.command_buffer import CommandBuffer, Command
from src.ssd_commands.ssd_command_action import SSDCommand


class WriteCommandAction(SSDCommand):
    def __init__(self, ssd_file_manager: SSDFileManager, command_buffer: CommandBuffer, *args):
        super().__init__(ssd_file_manager, command_buffer, *args)

        self.lba = self._arguments[0]
        self.value = self._arguments[1]

    def run(self) -> str:
        if not self.validate():
            self._ssd_file_manager.error()
            return "FAIL"

        # Buffer가 가득차 있다면 flush 수행
        if not self._command_buffer.is_empty_buffer_slot_existing():
            self.do_flush()
        
        # Command를 buffer에 추가
        self.append_command_into_command_buffer()

        return "PASS"

    def append_command_into_command_buffer(self):
        self._command_buffer.append(
            Command(
                order=-1,  # TODO: order를 특정할 수 있는 Logic 확인 필요 @정송화
                command_type="W",
                lba=self.lba,
                value=self.value
            )
        )

    def validate(self) -> bool:
        if len(self._arguments) != 2:
            return False

        self.lba, self.value = self._arguments

        if not self._ssd_file_manager._is_valid_lba(self.lba):
            return False

        if not self._ssd_file_manager._is_valid_value(self.value):
            return False

        return True

    def do_flush(self):
        """

        :return:
        """

        # command들을 fileManager를 통해 수행
        for command in self._command_buffer.command_buffers:
            match command.command_type:
                case "W":
                    self._ssd_file_manager.write(command.lba, command.value)
                case "E":
                    self._ssd_file_manager.erase(command.lba, command.size)

        # command buffer를 초기화
        self._command_buffer.initialize()

        return