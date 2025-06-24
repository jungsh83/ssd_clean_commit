from dataclasses import dataclass
from src.command_buffer.data_dict import EMPTY, ERASE, ERASE_VALUE, WRITE, WRITE_SIZE


class CommandBufferDataException(Exception):
    __module__ = 'builtins'

    def __init__(self, value):
        message = f"CommandBuffer 형식이 올바르지 않습니다: {value}"
        super().__init__(message)


@dataclass
class CommandBufferData:
    order: int = 0
    command_type: str = EMPTY
    lba: int | None = None
    value: str | None = None
    size: int | None = None

    def __post_init__(self):
        self.value = ERASE_VALUE if self.command_type == ERASE else self.value
        self.size = WRITE_SIZE if self.command_type == WRITE else self.size

    def __str__(self):
        if self.command_type == EMPTY:
            return f"{self.order}_{self.command_type}"
        elif self.command_type == WRITE:
            return f"{self.order}_{self.command_type}_{self.lba}_{self.value}"
        elif self.command_type == ERASE:
            return f"{self.order}_{self.command_type}_{self.lba}_{self.size}"
        return f"ERROR"

    @classmethod
    def create_write_command(cls, lba, value):
        return cls(command_type=WRITE, lba=lba, value=value)

    @classmethod
    def create_erase_command(cls, lba, size):
        return cls(command_type=ERASE, lba=lba, size=size)

    @classmethod
    def create_command_buffer_data_from_filename(cls, filename: str):
        if cls.is_invalid(filename):
            raise CommandBufferDataException(filename)

        parts = filename.split('_')
        order = int(parts[0])
        command_type = parts[1]
        if command_type == WRITE:
            command_buffer_data = cls.create_write_command(int(parts[2]), parts[3])
        elif command_type == ERASE:
            command_buffer_data = cls.create_erase_command(int(parts[2]), int(parts[3]))
        else:
            command_buffer_data = cls()

        command_buffer_data.order = order
        return command_buffer_data

    @classmethod
    def is_invalid(cls, filename):
        parts = filename.split('_')

        if len(parts) < 2:
            return True
        command_type = parts[1]
        if command_type != EMPTY and len(parts) < 4:
            return True
        if command_type not in [EMPTY, WRITE, ERASE]:
            return True

        return False

    @property
    def start_lba(self):
        return self.lba

    @property
    def end_lba(self):
        return self.lba + self.size
