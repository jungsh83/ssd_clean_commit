import sys
from src.ssd_file_manager import SSDFileManager
from src.ssd_commands.ssd_command import InvalidArgumentException
from src.command_buffer.command_buffer_handler import CommandBufferHandler
from src.ssd_commands.ssd_read import ReadSSDCommand
from src.ssd_commands.ssd_write import WriteSSDCommand
from src.ssd_commands.ssd_erase import EraseSSDCommand
from src.ssd_commands.ssd_flush import FlushSSDCommand

SSD_COMMANDS = {
    'R': ReadSSDCommand,
    'W': WriteSSDCommand,
    'E': EraseSSDCommand,
    'F': FlushSSDCommand,
}


class Invoker:
    def __init__(self):
        self.command = None

    def set_command(self, command):
        self.command = command

    def run(self):
        return self.command.execute()


def main(args: list[str]):
    if not args:
        SSDFileManager().error()
        return

    command_str = args[0]
    command_args = args[1:]

    command_class = SSD_COMMANDS.get(command_str)
    if not command_class:
        SSDFileManager().error()
        return

    command = command_class(SSDFileManager(), CommandBufferHandler(), *command_args)

    remote_controller = Invoker()
    remote_controller.set_command(command)

    try:
        remote_controller.run()
    except InvalidArgumentException:
        pass


if __name__ == "__main__":
    main(sys.argv[1:])
