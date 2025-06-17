import os


class VirtualSSD:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # src/ssd.py → 프로젝트 루트
    NAND_PATH = os.path.join(BASE_DIR, 'data', 'ssd_nand.txt')
    OUTPUT_PATH = os.path.join(BASE_DIR, 'data', 'ssd_output.txt')
    LBA_COUNT = 100

    def __init__(self):
        self._initialize_nand_if_needed()

    def _initialize_nand_if_needed(self):
        os.makedirs(os.path.dirname(self.NAND_PATH), exist_ok=True)
        if not os.path.exists(self.NAND_PATH):
            with open(self.NAND_PATH, 'w') as f:
                for _ in range(self.LBA_COUNT):
                    f.write('0x00000000\n')

    def read(self, lba: int) -> str:
        """지정 LBA에서 4 Byte 값을 읽어온다."""
        # 아직 구현 안 됨 → 테스트가 실패해야 정상
        return "0x00000000"

    def write(self, lba: int, value: str) -> None:
        if not (0 <= lba < self.LBA_COUNT):
            with open(self.OUTPUT_PATH, 'w') as f:
                f.write('ERROR')
            return
        data_lines = self._load_nand()
        data_lines[lba] = value
        self._save_nand(data_lines)

    def _save_nand(self, data_lines: list[str]) -> None:
        with open(self.NAND_PATH, 'w') as f:
            f.writelines([line + '\n' for line in data_lines])

    def _load_nand(self) -> list[str]:
        with open(self.NAND_PATH, 'r') as f:
            data_lines = [line.strip() for line in f.readlines()]
        return data_lines
