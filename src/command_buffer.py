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


class CommandBuffer:
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
        # 비어 있는 슬롯 찾기
        insert_order = 0
        for command in self.command_buffers:
            if command.command_type == 'I':
                new_command.order = command.order
                break
            else:
                insert_order += 1

        self._command_buffers[insert_order] = new_command

    def append(self, command: Command):
        try:
            self._append_command(command)
            self._ignore_command()
            self._merge_erase()
            self._update_command_buffers_to_file_name()
        except Exception:
            raise CommandBufferException

    def read_all(self):
        result: list[Command] = []
        # 파일 리스트 읽어서 result에 담아서 return 하기
        # 디렉토리나 파일이 없을 경우 initialize() 호출
        self.initialize()
        return result

    def _ignore_command(self):
        # 삭제될 커맨드를 찾아서 삭제
        pass

    def _merge_erase(self):
        # 머지할 커맨드를 찾아서 머지, 꼭 작은 order에 머지해야 함
        pass

    def _update_command_buffers_to_file_name(self):
        # self._command_buffers의 내용을 파일명으로 작성하기
        pass

    def initialize(self):
        # 디렉토리가 없을 경우 디렉토리 생성 ../buffer
        # 파일이 없을 경우 파일 생성 ../buffer/1_empty ~ ../buffer/5_empty
        init_command_buffers = [
            Command(order=1),
            Command(order=2),
            Command(order=3),
            Command(order=4),
            Command(order=5)
        ]
        pass
