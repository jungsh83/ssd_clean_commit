import sys
from src.ssd_file_manager import SSDFileManager
from src.ssd_commands.ssd_command_action import InvalidArgumentException
from src.command_buffer import CommandBuffer
from src.ssd_commands.ssd_read import ReadCommand

# Command 구현 전에 test 구동을 위해 임시로 None으로 처리해놨습니다
WriteCommand = None
EraseCommand = None
FlushCommand = None


SSD_COMMANDS = {
    'R': ReadCommand,
    'W': WriteCommand,
    'E': EraseCommand,
    'F': FlushCommand,
}

def main(args: list[str]):
    if not args:
        SSDFileManager().error()
        return

    command_str = args[0]
    command_args = args[1:]

    CommandClass = SSD_COMMANDS.get(command_str)
    if not CommandClass:
        SSDFileManager().error()
        return

    command = CommandClass(SSDFileManager(), CommandBuffer(), *command_args)

    try:
        command.run()
    except InvalidArgumentException:
        pass

if __name__ == "__main__":
    main(sys.argv[1:])