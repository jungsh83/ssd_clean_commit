from pathlib import Path

from src.command_buffer_data import MAX_SIZE_OF_COMMAND_BUFFERS, CommandBufferData, CommandBufferDataException


class CommandBufferFileManager:
    BASE_DIR = Path(__file__).parent.parent
    COMMAND_BUFFER_DIR_PATH = BASE_DIR / 'buffer'

    def __init__(self):
        if self._is_not_initialized():
            self._initialize_file()

    def _initialize_file(self):
        temp_command_buffers = [CommandBufferData(order=index + 1) for index in range(MAX_SIZE_OF_COMMAND_BUFFERS)]
        self.COMMAND_BUFFER_DIR_PATH.mkdir(parents=True, exist_ok=True)
        for command in temp_command_buffers:
            filename = str(command)
            command_path = self.COMMAND_BUFFER_DIR_PATH / filename
            command_path.touch()

    def _is_not_initialized(self):
        if not self.COMMAND_BUFFER_DIR_PATH.exists():
            return True

        files_in_dir = [file for file in self.COMMAND_BUFFER_DIR_PATH.iterdir() if file.is_file()]
        if not files_in_dir:
            return True

        return False

    def read_command_buffers_from_file_name(self):
        result: list[CommandBufferData] = []

        files_in_dir = [file for file in self.COMMAND_BUFFER_DIR_PATH.iterdir() if file.is_file()]
        for filepath in files_in_dir:
            command = CommandBufferData.create_command_buffer_data_from_filename(filepath.name)
            result.append(command)
        return result

    def write_command_buffers_to_file_name(self, new_command_buffers):

        files_in_dir = [file for file in self.COMMAND_BUFFER_DIR_PATH.iterdir() if file.is_file()]
        for current_file_path in files_in_dir:
            current_command = CommandBufferData.create_command_buffer_data_from_filename(current_file_path.name)

            for new_command in new_command_buffers:
                if new_command.order == current_command.order:
                    new_filename = str(new_command)
                    new_file_path = self.COMMAND_BUFFER_DIR_PATH / new_filename
                    try:
                        current_file_path.rename(new_file_path)
                    except Exception:
                        raise CommandBufferDataException(f"CommandBuffer 업데이트를 실패했습니다.: {new_file_path}")
