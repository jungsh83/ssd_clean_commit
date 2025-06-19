import os
import sys
from ssd_file_manager import SSDFileManager


def main(args: list[str]):
    ssd = SSDFileManager()

    if len(args) == 2 and args[0] == ssd.COMMAND_READ:
        lba_str = args[1]
        if not lba_str.isdigit():
            ssd.error()
            return
        lba = int(lba_str)
        ssd.read(lba)

    elif len(args) == 3 and args[0] == ssd.COMMAND_WRITE:
        lba_str, value = args[1], args[2]
        if not lba_str.isdigit():
            ssd.error()
            return
        lba = int(lba_str)
        ssd.write(lba, value)

    else:
        ssd.error()


if __name__ == "__main__":
    main(sys.argv[1:])
