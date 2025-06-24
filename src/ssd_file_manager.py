import os
from src.data_dict import LBA_COUNT, ERROR_TEXT, DEFAULT_VAL, LBA_START_INDEX


class SSDFileManager:
    _instance = None  # 싱글톤 인스턴스 저장 변수

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    NAND_PATH = os.path.join(BASE_DIR, 'data', 'ssd_nand.txt')
    OUTPUT_PATH = os.path.join(BASE_DIR, 'data', 'ssd_output.txt')

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SSDFileManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self._initialize_nand_if_needed()

    @classmethod
    def _reset_instance(cls):
        """테스트 전용: 싱글톤 인스턴스를 리셋"""
        cls._instance = None

    def _initialize_nand_if_needed(self):
        os.makedirs(os.path.dirname(self.NAND_PATH), exist_ok=True)
        if not os.path.exists(self.NAND_PATH):
            with open(self.NAND_PATH, 'w', encoding='utf-8') as f:
                for _ in range(LBA_COUNT):
                    f.write(DEFAULT_VAL + '\n')

        with open(self.OUTPUT_PATH, 'w', encoding='utf-8') as f:
            pass

    def _load_nand(self) -> list[str]:
        with open(self.NAND_PATH, 'r', encoding='utf-8') as f:
            return [line.rstrip('\n') for line in f]

    def _save_nand(self, data_lines: list[str]) -> None:
        with open(self.NAND_PATH, 'w', encoding='utf-8') as f:
            f.writelines(line + '\n' for line in data_lines)

    def read(self, lba: int) -> str:
        value = self._load_nand()[lba]
        with open(self.OUTPUT_PATH, 'w', encoding='utf-8') as f:
            f.write(value + '\n')
        return value

    def write(self, lba: int, value: str) -> None:
        data = self._load_nand()
        data[lba] = value
        self._save_nand(data)
        with open(self.OUTPUT_PATH, 'w', encoding='utf-8') as f:
            pass

    def erase(self, lba: int, size: int) -> None:
        data = self._load_nand()
        for i in range(lba, lba + size):
            data[i] = DEFAULT_VAL
        self._save_nand(data)
        with open(self.OUTPUT_PATH, 'w', encoding='utf-8') as f:
            pass

    def error(self):
        with open(self.OUTPUT_PATH, 'w', encoding='utf-8') as f:
            f.write(ERROR_TEXT)

    # SSD Read Command에서 fast read 로 값을 읽어온 경우, SSDFileManger의 write_output 메서드를 호출
    def write_output(self, value: str):
        with open(self.OUTPUT_PATH, 'w', encoding='utf-8') as f:
            f.write(value + '\n')
