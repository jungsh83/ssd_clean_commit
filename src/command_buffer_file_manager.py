import os
from pathlib import Path

from src.command_buffer_data import CommandBufferData, CommandBufferException


class CommandBufferFileManager:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    COMMAND_BUFFER_DIR_PATH = Path(os.path.join(BASE_DIR, 'buffer'))

    def update_command_buffers_to_file_name(self, command_buffers):
        current_files = list(self.COMMAND_BUFFER_DIR_PATH.iterdir())
        old_file_path = None

        for new_command in command_buffers:
            for file_path in current_files:
                if file_path.is_file():
                    try:
                        parsed_command = CommandBufferData.from_filename(file_path.name)
                        if parsed_command.order == new_command.order:
                            old_file_path = file_path
                            break
                    except Exception:
                        continue

            if not old_file_path:
                return False

            new_filename = str(new_command)
            new_file_path = self.COMMAND_BUFFER_DIR_PATH / new_filename

            try:
                old_file_path.rename(new_file_path)
            except Exception:
                raise CommandBufferException(f"CommandBuffer 업데이트를 실패했습니다.: {new_file_path}")
        return None


    def initialize_file_name(self, command_buffers):
        self.COMMAND_BUFFER_DIR_PATH.mkdir(parents=True, exist_ok=True)
        if not any(self.COMMAND_BUFFER_DIR_PATH.iterdir()):
            print("디렉토리가 비어있어 초기 'empty' 파일들을 생성합니다.")
            for command in command_buffers:
                filename = str(command)
                command_path = self.COMMAND_BUFFER_DIR_PATH / filename
                command_path.touch()
        else:
            self.update_command_buffers_to_file_name(command_buffers)