from src.ssd import VirtualSSD
from command_action import CommandAction
class FullRead(CommandAction):

    command_name = ["fullread", "fr"]

    def __init__(self, ssd:VirtualSSD):
        self._ssd = ssd
    def validate(self) -> bool:
        """fullread 는 인자를 받지 않는다."""
        return len(self._arguments) == 0
    def run(self) -> None:
        """LBA 0~99 값을 표준 출력으로 내보낸다."""
        for lba in range(self._ssd_driver.LBA_COUNT):       # 100개  :contentReference[oaicite:1]{index=1}
            print(self._ssd_driver.read(lba))               # read() 가 값·파일출력까지 처리
