import os

class VirtualSSD:
    """칸 100개짜리 가상 SSD. 아직 로직은 안 넣었음."""

    NUM_BLOCKS = 100                # LBA 0 ~ 99
    DEFAULT_VAL = "0x00000000"

    def __init__(self,
                 nand_file="./data/ssd_nand.txt",
                 output_file="./data/ssd_output.txt"):
        # 경로를 문자열 그대로 사용
        self.nand_file   = nand_file
        self.output_file = output_file

    def read(self, lba: int) -> str:
        # ── 1) 범위 체크 ─────────────────────────────────────────────
        if not 0 <= lba < self.NUM_BLOCKS:
            with open(self.output_file, "w", encoding="utf-8") as f:
                f.write("ERROR\n")
            return "ERROR"

        # ── 2) 값 읽기 ───────────────────────────────────────────────
        value = self.DEFAULT_VAL
        try:
            with open(self.nand_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
            raw_line = lines[lba]
            # expected format: "idx: 0xXXXXXXXX" → take substring after ':'
            value = raw_line.split(":", 1)[1].strip()
        except Exception:
            # file missing, index error, parse error → keep DEFAULT_VAL
            pass

        # ── 3) 파일 기록 ─────────────────────────────────────────────
        with open(self.output_file, "w", encoding="utf-8") as f:
            f.write(value + "\n")
        return value


    def write(self, lba: int, value: str) -> None:
        """지정 LBA에 4 Byte 값을 기록한다."""
        # 아직 구현 안 됨
        return "0x12345678"