from dataclasses import dataclass

ERASE_VALUE = "0x00000000"
WRITE_SIZE = 1
ERASE = 'E'
WRITE = 'W'
EMPTY = 'empty'


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

    def __str__(self):
        if self.command_type == EMPTY:
            return f"{self.order}_{self.command_type}"
        elif self.command_type == WRITE:
            return f"{self.order}_{self.command_type}_{self.lba}_{self.value}"
        elif self.command_type == ERASE:
            return f"{self.order}_{self.command_type}_{self.lba}_{self.size}"
        return f"ERROR"

    @classmethod
    def create_command_buffer_data_from_filename(cls, filename: str):
        if cls.is_invalid(filename):
            raise CommandBufferDataException(filename)

        parts = filename.split('_')
        order = int(parts[0])
        command_type = parts[1]
        if command_type == WRITE:
            return cls(order=order, command_type=WRITE, lba=int(parts[2]), value=parts[3], size=WRITE_SIZE)

        elif command_type == ERASE:
            return cls(order=order, command_type=ERASE, lba=int(parts[2]), value=ERASE_VALUE, size=int(parts[3]))

        return cls(order=order, command_type=EMPTY)

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
