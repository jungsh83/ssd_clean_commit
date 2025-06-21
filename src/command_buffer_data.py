from dataclasses import dataclass

ERASE_VALUE = "0x00000000"
WRITE_SIZE = 1
ERASE = 'empty'
WRITE = 'W'
EMPTY = 'I'


class CommandBufferException(Exception):
    __module__ = 'builtins'


@dataclass
class CommandBufferData:
    order: int = -1
    command_type: str = EMPTY
    lba: int = -1
    value: str = ""
    size: int = -1

    def __str__(self):
        if self.command_type == EMPTY:
            return f"{self.order}_{self.command_type}"
        elif self.command_type == WRITE:
            return f"{self.order}_{self.command_type}_{self.lba}_{self.value}"
        elif self.command_type == ERASE:
            return f"{self.order}_{self.command_type}_{self.lba}_{self.size}"
        return f"ERROR"

    @classmethod
    def from_filename(cls, filename: str):
        parts = filename.split('_')
        if len(parts) < 2:
            raise CommandBufferException(f"CommandBuffer 형식이 올바르지 않습니다: {filename}")

        command_type = parts[1]
        if command_type != EMPTY and len(parts) < 4:
            raise CommandBufferException(f"CommandBuffer 형식이 올바르지 않습니다: {filename}")

        if command_type not in [EMPTY, WRITE, ERASE]:
            raise CommandBufferException(f"CommandBuffer 형식이 올바르지 않습니다: {filename}")

        order = int(parts[0])
        if command_type == WRITE:
            return cls(order=order, command_type=command_type, lba=int(parts[2]), value=parts[3], size=WRITE_SIZE)

        elif command_type == ERASE:
            return cls(order=order, command_type=command_type, lba=int(parts[2]), value=ERASE_VALUE, size=int(parts[3]))

        return cls(order=order)

    @property
    def erase_start_lba(self):
        return self.lba

    @property
    def erase_end_lba(self):
        return self.lba + self.size
