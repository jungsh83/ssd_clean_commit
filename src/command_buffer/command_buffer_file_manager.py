from pathlib import Path
from src.command_buffer.data_dict import MAX_SIZE_OF_COMMAND_BUFFERS
from src.command_buffer.command_buffer_data import CommandBufferData


class CommandBufferFileManager:
    BASE_DIR = Path(__file__).parent.parent.parent
    COMMAND_BUFFER_DIR_PATH = BASE_DIR / 'buffer'

    def __init__(self):
        if self._is_not_initialized():
            self._initialize_file()

    def _initialize_file(self):
        temp_command_buffers = [CommandBufferData(order=index + 1) for index in range(MAX_SIZE_OF_COMMAND_BUFFERS)]
        self.COMMAND_BUFFER_DIR_PATH.mkdir(parents=True, exist_ok=True)
        for command in temp_command_buffers:
            (self.COMMAND_BUFFER_DIR_PATH / str(command)).touch()

    def _is_not_initialized(self):
        if not self.COMMAND_BUFFER_DIR_PATH.exists():
            return True

        if not self._get_files_in_command_buffer_dir():
            return True

        return False

    def read_command_buffers_from_file_name(self):
        result: list[CommandBufferData] = []

        for filepath in self._get_files_in_command_buffer_dir():
            result.append(CommandBufferData.create_command_buffer_data_from_filename(filepath.name))
        return result

    def write_command_buffers_to_file_name(self, new_command_buffers):

        for current_file_path in self._get_files_in_command_buffer_dir():
            current_command = CommandBufferData.create_command_buffer_data_from_filename(current_file_path.name)

            for new_command in new_command_buffers:
                if new_command.order == current_command.order:
                    current_file_path.rename(self.COMMAND_BUFFER_DIR_PATH / str(new_command))

    def _get_files_in_command_buffer_dir(self):
        files_in_dir = [file for file in self.COMMAND_BUFFER_DIR_PATH.iterdir() if file.is_file()]
        return files_in_dir
