
class VirtualSSD:
    """칸 100개짜리 가상 SSD. 아직 로직은 안 넣었음."""

    NUM_BLOCKS = 100                # LBA 0 ~ 99

    def __init__(self,
                 nand_file="./data/ssd_nand.txt",
                 output_file="ssd_output.txt"):
        # 경로를 문자열 그대로 사용
        self.nand_file   = nand_file
        self.output_file = output_file

    def read(self, lba: int) -> str:
        """지정 LBA에서 4 Byte 값을 읽어온다."""
        # 아직 구현 안 됨 → 테스트가 실패해야 정상
        return "0x00000000"

    def write(self, lba: int, value: str) -> None:
        """지정 LBA에 4 Byte 값을 기록한다."""
        # 아직 구현 안 됨
        return "0x12345678"