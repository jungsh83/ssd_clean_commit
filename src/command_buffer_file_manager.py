import os
from pathlib import Path

from src.command_buffer_data import CommandBufferData, CommandBufferDataException


class CommandBufferFileManager:
    BASE_DIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    COMMAND_BUFFER_DIR_PATH = BASE_DIR / 'buffer'

    def initialize_file_name(self, command_buffers):
        self.COMMAND_BUFFER_DIR_PATH.mkdir(parents=True, exist_ok=True)
        if not any(self.COMMAND_BUFFER_DIR_PATH.iterdir()):
            print("디렉토리가 비어있어 초기 'empty' 파일들을 생성합니다.")
            for command in command_buffers:
                filename = str(command)
                command_path = self.COMMAND_BUFFER_DIR_PATH / filename
                command_path.touch()

    def is_not_initialized(self):
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

    def update_command_buffers_to_file_name(self, new_command_buffers):

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
