import os
import sys


class VirtualSSD:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    NAND_PATH = os.path.join(BASE_DIR, 'data', 'ssd_nand.txt')
    OUTPUT_PATH = os.path.join(BASE_DIR, 'data', 'ssd_output.txt')

    LBA_COUNT = 100  # LBA 0~99
    DEFAULT_VAL = "0x00000000"
    ERROR_TEXT = 'ERROR'
    COMMAND_READ = "R"
    COMMAND_WRITE = "W"

    def __init__(self):
        self._initialize_nand_if_needed()

    def _initialize_nand_if_needed(self):
        os.makedirs(os.path.dirname(self.NAND_PATH), exist_ok=True)
        if not os.path.exists(self.NAND_PATH):
            with open(self.NAND_PATH, 'w', encoding='utf-8') as f:
                for _ in range(self.LBA_COUNT):
                    f.write(self.DEFAULT_VAL + '\n')

    def _load_nand(self) -> list[str]:
        with open(self.NAND_PATH, 'r', encoding='utf-8') as f:
            return [line.rstrip('\n') for line in f]

    def _save_nand(self, data_lines: list[str]) -> None:
        with open(self.NAND_PATH, 'w', encoding='utf-8') as f:
            f.writelines(line + '\n' for line in data_lines)

    def read(self, lba: int) -> str:
        if not 0 <= lba < self.LBA_COUNT:
            self._write_error()
            return self.ERROR_TEXT

        value = self._load_nand()[lba]

        with open(self.OUTPUT_PATH, 'w', encoding='utf-8') as f:
            f.write(value + '\n')
        return value

    def write(self, lba: int, value: str) -> None:
        if not 0 <= lba < self.LBA_COUNT:
            self._write_error()
            return
        data = self._load_nand()
        data[lba] = value
        self._save_nand(data)
        with open(self.OUTPUT_PATH, 'w', encoding='utf-8') as f:
            pass  # 명령 성공 시 빈 파일 생성

    def _write_error(self):
        with open(self.OUTPUT_PATH, 'w', encoding='utf-8') as f:
            f.write(self.ERROR_TEXT)


def main(args: list[str]):
    ssd = VirtualSSD()

    if len(args) == 2 and args[0] == ssd.COMMAND_READ:
        try:
            lba = int(args[1])
            ssd.read(lba)
        except (ValueError, IndexError):
            ssd._write_error()

    elif len(args) == 3 and args[0] == ssd.COMMAND_WRITE:
        try:
            lba = int(args[1])
            value = args[2]
            ssd.write(lba, value)
        except (ValueError, IndexError):
            ssd._write_error()

    else:
        ssd._write_error()


if __name__ == "__main__":
    main(sys.argv[1:])
