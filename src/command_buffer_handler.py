import os
from pathlib import Path

from src.command_buffer_data import ERASE_VALUE, ERASE, WRITE, EMPTY, CommandBufferException, CommandBufferData
from src.command_buffer_optimizer import CommandBufferOptimizer, IgnoreCommandStrategy, MergeEraseStrategy


class CommandBufferHandler:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    COMMAND_BUFFER_DIR_PATH = Path(os.path.join(BASE_DIR, 'buffer'))

    def __init__(self):
        self._command_buffers = self.read_all()

    @property
    def command_buffers(self):
        return self._command_buffers

    def fast_read(self, lba: int) -> str | None:
        for command in self.command_buffers:
            if command.command_type == WRITE and command.lba == lba:
                return command.value
            elif command.command_type == ERASE and (command.erase_start_lba <= lba < command.erase_end_lba):
                return ERASE_VALUE
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
            raise CommandBufferException("남아 있는 Buffer Slot이 없습니다.")

        new_command.order = insert_order + 1
        self._command_buffers[insert_order] = new_command

    def append(self, command: CommandBufferData):
        try:
            new_command = command
            if command.command_type == WRITE and command.value == ERASE_VALUE:
                new_command = CommandBufferData(command_type=ERASE, lba=command.lba, size=1)

            self._append_command(new_command)
            optimizer = CommandBufferOptimizer(IgnoreCommandStrategy())
            self._command_buffers = optimizer.optimize(self.command_buffers)
            optimizer = CommandBufferOptimizer(MergeEraseStrategy())
            self._command_buffers = optimizer.optimize(self.command_buffers)

            self._update_command_buffers_to_file_name()
        except CommandBufferException as e:
            raise e
        except Exception:
            raise CommandBufferException("Buffer 처리 실패하였습니다.")

    def read_all(self):
        result: list[CommandBufferData] = []

        if not self.COMMAND_BUFFER_DIR_PATH.exists():
            self.initialize()

        files_in_dir = [file for file in self.COMMAND_BUFFER_DIR_PATH.iterdir() if file.is_file()]

        if not files_in_dir:
            self.initialize()
            files_in_dir = [file for file in self.COMMAND_BUFFER_DIR_PATH.iterdir() if file.is_file()]

        for filepath in files_in_dir:
            try:
                command = CommandBufferData.from_filename(filepath.name)
                result.append(command)
            except Exception as e:
                raise CommandBufferException(f"CommandBuffer 형식이 올바르지 않습니다: {files_in_dir}")

        result.sort(key=lambda cmd: cmd.order)
        return result

    def _update_command_buffers_to_file_name(self):
        current_files = list(self.COMMAND_BUFFER_DIR_PATH.iterdir())
        old_file_path = None

        for new_command in self.command_buffers:
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

    def initialize(self):
        self._command_buffers = [
            CommandBufferData(order=1),
            CommandBufferData(order=2),
            CommandBufferData(order=3),
            CommandBufferData(order=4),
            CommandBufferData(order=5)
        ]

        self.COMMAND_BUFFER_DIR_PATH.mkdir(parents=True, exist_ok=True)
        if not any(self.COMMAND_BUFFER_DIR_PATH.iterdir()):
            print("디렉토리가 비어있어 초기 'empty' 파일들을 생성합니다.")
            for command in self._command_buffers:
                filename = str(command)
                command_path = self.COMMAND_BUFFER_DIR_PATH / filename
                command_path.touch()
        else:
            self._update_command_buffers_to_file_name()
