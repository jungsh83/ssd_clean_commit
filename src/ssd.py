import os
import sys


class VirtualSSD:
    # 프로젝트 루트/data/ssd_*.txt
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    NAND_PATH = os.path.join(BASE_DIR, 'data', 'ssd_nand.txt')
    OUTPUT_PATH = os.path.join(BASE_DIR, 'data', 'ssd_output.txt')

    LBA_COUNT = 100  # LBA 0~99
    DEFAULT_VAL = "0x00000000"  # 읽기 실패 시 기본값

    def __init__(self):
        self._initialize_nand_if_needed()

    # ───────── 내부 유틸 ──────────────────────────────────────────────
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

    # ───────── 퍼블릭 API ────────────────────────────────────────────
    def read(self, lba: int) -> str:
        # 1) 범위 체크
        if not 0 <= lba < self.LBA_COUNT:
            with open(self.OUTPUT_PATH, 'w', encoding='utf-8') as f:
                f.write('ERROR\n')
            return 'ERROR'

        # 2) 값 읽기
        try:
            value = self._load_nand()[lba]
        except Exception:  # 파일 없음·인덱스 오류 등
            value = self.DEFAULT_VAL

        # 3) 결과 기록
        with open(self.OUTPUT_PATH, 'w', encoding='utf-8') as f:
            f.write(value + '\n')
        return value

    def write(self, lba: int, value: str) -> None:
        if not 0 <= lba < self.LBA_COUNT:
            with open(self.OUTPUT_PATH, 'w', encoding='utf-8') as f:
                f.write('ERROR')
            return
        data = self._load_nand()
        data[lba] = value
        self._save_nand(data)
        with open(self.OUTPUT_PATH, 'w', encoding='utf-8') as f:
            pass


if __name__ == "__main__":

    args = sys.argv[1:]
    ssd = VirtualSSD()


    def write_error():
        with open(ssd.OUTPUT_PATH, 'w', encoding='utf-8') as f:
            f.write("ERROR\n")


    if len(args) == 2 and args[0] == 'R':
        try:
            lba = int(args[1])
            ssd.read(lba)
        except Exception:
            write_error()

    elif len(args) == 3 and args[0] == 'W':
        try:
            lba = int(args[1])
            value = args[2]
            ssd.write(lba, value)
        except Exception:
            write_error()

    else:
        write_error()
