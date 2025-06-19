import os
from pathlib import Path
from dataclasses import dataclass


class CommandBufferException(Exception):
    __module__ = 'builtins'


@dataclass
class Command:
    order: int = -1
    command_type: str = "I"
    lba: int = -1
    value: str = ""
    size: int = -1

    def __str__(self):
        if self.command_type == 'I':
            return f"{self.order}_empty"
        elif self.command_type == 'W':
            return f"{self.order}_{self.command_type}_{self.lba}_{self.value}"
        elif self.command_type == 'E':
            return f"{self.order}_{self.command_type}_{self.lba}_{self.size}"
        return f"ERROR"

    @classmethod
    def from_filename(cls, filename: str):
        parts = filename.split('_')
        if len(parts) < 2:
            raise CommandBufferException(f"CommandBuffer 형식이 올바르지 않습니다: {filename}")

        order = int(parts[0])
        command_type = parts[1]

        if command_type == 'empty':
            return cls(order=order)

        if len(parts) < 4:
            raise CommandBufferException(f"CommandBuffer 형식이 올바르지 않습니다: {filename}")

        if command_type == 'W':
            return cls(order=order, command_type=command_type, lba=int(parts[2]), value=parts[3])

        elif command_type == 'E':
            return cls(order=order, command_type=command_type, lba=int(parts[2]), size=int(parts[3]))

        else:
            raise CommandBufferException(f"CommandBuffer 형식이 올바르지 않습니다: {filename}")


class CommandBuffer:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    COMMAND_BUFFER_DIR_PATH = Path(os.path.join(BASE_DIR, 'buffer'))

    def __init__(self):
        self._command_buffers = self.read_all()

    @property
    def command_buffers(self):
        return self._command_buffers

    def fast_read(self, lba: int) -> str | None:
        for command in self.command_buffers:
            if command.command_type == 'W' and command.lba == lba:
                return command.value
            elif command.command_type == 'E' and (command.lba <= lba < command.lba + command.size):
                return "0x00000000"
        return None

    def is_empty_buffer_slot_existing(self) -> bool:
        for command in self.command_buffers:
            if command.command_type == 'I':
                return True
        return False

    def _append_command(self, new_command):
        insert_order = 0
        for command in self.command_buffers:
            if command.command_type == 'I':
                new_command.order = command.order
                break
            else:
                insert_order += 1

        if insert_order >= 5:
            raise CommandBufferException("남아 있는 Buffer Slot이 없습니다.")

        new_command.order = insert_order + 1
        self._command_buffers[insert_order] = new_command

    def append(self, command: Command):
        try:
            new_command = command
            if command.command_type == 'W' and command.value == '0x00000000':
                new_command = Command(command_type='E', lba=command.lba, size=1)

            self._append_command(new_command)
            self._ignore_command()
            self._merge_erase()
            self._update_command_buffers_to_file_name()
        except CommandBufferException as e:
            raise e
        except Exception:
            raise CommandBufferException("Buffer 처리 실패하였습니다.")

    def read_all(self):
        result: list[Command] = []

        files_in_dir = [file for file in self.COMMAND_BUFFER_DIR_PATH.iterdir() if file.is_file()]

        if not files_in_dir:
            self.initialize()
            files_in_dir = [file for file in self.COMMAND_BUFFER_DIR_PATH.iterdir() if file.is_file()]

        for filepath in files_in_dir:
            try:
                command = Command.from_filename(filepath.name)
                result.append(command)
            except Exception as e:
                raise CommandBufferException(f"CommandBuffer 형식이 올바르지 않습니다: {files_in_dir}")

        result.sort(key=lambda cmd: cmd.order)
        return result

    def _ignore_command(self):
        result: list[Command] = []
        new_order = 0
        for target_index, target_command in enumerate(self.command_buffers):
            lbas: set[int] = set()
            if target_command.command_type == 'W':
                lbas.add(target_command.lba)
            elif target_command.command_type == 'E':
                lbas = set([i for i in range(target_command.lba, target_command.lba + target_command.size)])
                lbas.add(target_command.lba)
            for overwrite_index in range(target_index + 1, 5):
                overwrite_command = self.command_buffers[overwrite_index]
                if overwrite_command.command_type == 'W':
                    if overwrite_command.lba in lbas:
                        lbas.remove(overwrite_command.lba)
                elif overwrite_command.command_type == 'E':
                    for overwrite_lba in range(overwrite_command.lba, overwrite_command.lba + overwrite_command.size):
                        if overwrite_lba in lbas:
                            lbas.remove(overwrite_lba)
            if lbas:
                new_order += 1
                result.append(
                    Command(order=new_order, command_type=target_command.command_type, lba=target_command.lba,
                            value=target_command.value,
                            size=target_command.size))

        for i in range(new_order + 1, 6):
            result.append(Command(order=i))

        self._command_buffers = result

    def _merge_erase(self):
        result: list[Command] = []
        new_order = 0
        merged_command_orders: set[int] = set()
        for target_index, target_command in enumerate(self.command_buffers):
            if target_command.command_type != 'E':
                new_order += 1
                result.append(
                    Command(order=new_order, command_type=target_command.command_type, lba=target_command.lba,
                            value=target_command.value,
                            size=target_command.size))
                continue
            elif target_command.order in merged_command_orders:
                continue
            new_lba = target_command.lba
            new_size = target_command.size
            for overwrite_index in range(target_index + 1, 5):
                overwrite_command = self.command_buffers[overwrite_index]
                if overwrite_command.command_type != 'E':
                    continue
                if new_lba <= overwrite_command.lba + overwrite_command.size and \
                        new_lba + new_size >= overwrite_command.lba:

                    new_lba = min(new_lba, overwrite_command.lba)
                    new_size = max(new_lba + new_size,
                                   overwrite_command.lba + overwrite_command.size) \
                               - new_lba
                    merged_command_orders.add(overwrite_command.order)

            while new_size > 10:
                new_order += 1
                result.append(
                    Command(order=new_order, command_type=target_command.command_type, lba=new_lba,
                            value=target_command.value,
                            size=10))
                new_lba += 10
                new_size -= 10
            new_order += 1
            result.append(
                Command(order=new_order, command_type=target_command.command_type, lba=new_lba,
                        value=target_command.value,
                        size=new_size))

        for i in range(new_order + 1, 6):
            result.append(Command(order=i))

        as_is_count = 0
        for command in self.command_buffers:
            if command.command_type == 'E':
                as_is_count += 1

        to_be_count = 0
        for command in result:
            if command.command_type == 'E':
                to_be_count += 1

        if as_is_count > to_be_count:
            self._command_buffers = result

    def _update_command_buffers_to_file_name(self):
        current_files = list(self.COMMAND_BUFFER_DIR_PATH.iterdir())
        old_file_path = None

        for new_command in self.command_buffers:
            for file_path in current_files:
                if file_path.is_file():
                    try:
                        parsed_command = Command.from_filename(file_path.name)
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
            Command(order=1),
            Command(order=2),
            Command(order=3),
            Command(order=4),
            Command(order=5)
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
