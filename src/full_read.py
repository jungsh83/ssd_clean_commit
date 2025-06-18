# src/full_read.py
from __future__ import annotations

from src.command_action import CommandAction


class FullRead(CommandAction):
    """
    fullread / fr
    ──────────────
    • 인자를 받지 않는다.
    • LBA 0 ~ LBA_COUNT-1 값을 순차적으로 읽어 한 줄씩 출력한다.
    """

    command_name = ["fullread", "fr"]

    # CommandAction 에서 _ssd_driver / _arguments 를 셋업해 주므로
    # 여기서는 super().__init__ 만 호출하면 충분하다.
    def __init__(self, ssd_driver, *arguments: str) -> None:
        super().__init__(ssd_driver, *arguments)

    # ────────────────────────────────────────────────────────
    # validate
    # ────────────────────────────────────────────────────────
    def validate(self) -> bool:
        """fullread 는 **절대** 인자를 받지 않는다."""
        return not self._arguments                        # 빈 리스트이면 True

    # ────────────────────────────────────────────────────────
    # 핵심 로직을 분리해 테스트·재사용성 향상
    # ────────────────────────────────────────────────────────
    def _dump_all(self) -> list[str]:
        """LBA 0 ~ 99 값을 읽어 리스트로 반환한다."""
        return [
            self._ssd_driver.read(lba)
            for lba in range(self._ssd_driver.LBA_COUNT)
        ]

    # ────────────────────────────────────────────────────────
    # run
    # ────────────────────────────────────────────────────────
    def run(self) -> None:
        if not self.validate():
            print("ERROR")
            return

        for value in self._dump_all():
            print(value)
