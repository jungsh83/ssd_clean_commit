import os

class VirtualSSD:
    """칸 100개짜리 가상 SSD. 아직 로직은 안 넣었음."""

    NUM_BLOCKS = 100                # LBA 0 ~ 99

    def __init__(self,
                 nand_file="./data/ssd_nand.txt",
                 output_file="./data/ssd_output.txt"):
        # 경로를 문자열 그대로 사용
        self.nand_file   = nand_file
        self.output_file = output_file

    def read(self, lba: int) -> str:
        # Green 단계용: 항상 기본값 반환 및 기록만 수행
        value = "0x00000000"
        # 출력 파일에 덮어쓰기 방식으로 한 줄 기록
        out_dir = os.path.dirname(self.output_file)
        if out_dir and not os.path.exists(out_dir):
            os.makedirs(out_dir, exist_ok=True)
        # 덮어쓰기 모드로 기록
        with open(self.output_file, 'w') as out:
            out.write(value + "\n")
        return value

    def write(self, lba: int, value: str) -> None:
        """지정 LBA에 4 Byte 값을 기록한다."""
        # 아직 구현 안 됨
        return "0x12345678"