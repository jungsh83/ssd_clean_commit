class VirtualSSD:
    """칸 100개짜리 가상 SSD. 아직 로직은 안 넣었음."""

    NUM_BLOCKS = 100                # LBA 0 ~ 99

    def __init__(self):
        # 나중에 실제 저장소(dict나 파일)에 연결할 예정
        pass

    def read(self, lba: int) -> str:
        """지정 LBA에서 4 Byte 값을 읽어온다."""
        # 아직 구현 안 됨 → 테스트가 실패해야 정상
        return "0x00000000"

    def write(self, lba: int, value: str) -> None:
        """지정 LBA에 4 Byte 값을 기록한다."""
        # 아직 구현 안 됨
        return "0x12345678"