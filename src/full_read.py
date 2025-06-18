# src/full_read.py
from src.command_action import CommandAction
from src.ssd import VirtualSSD

class FullRead(CommandAction):
    """LBA 0~99 전체 값을 표준 출력으로 내보내는 커맨드."""

    command_name = ["fullread", "fr"]

    # ----------------------------------------------------
    # 1) 시그니처: (ssd_driver, *arguments) 로 맞춰 주기
    # ----------------------------------------------------
    def __init__(self, ssd_driver: VirtualSSD, *arguments: str):
        super().__init__(ssd_driver, *arguments)   # 부모에게 위임

    # ----------------------------------------------------
    # 2) 인자 개수 유효성 검사
    # ----------------------------------------------------
    def validate(self) -> bool:
        return len(self._arguments) == 0           # fullread 는 인자 없음

    # ----------------------------------------------------
    # 3) run: validate 실패 시 "ERROR" 출력 후 종료
    # ----------------------------------------------------
    def run(self) -> None:
        if not self.validate():
            print("ERROR")
            return
        for lba in range(self._ssd_driver.LBA_COUNT):   # 0~99
            print(self._ssd_driver.read(lba))
