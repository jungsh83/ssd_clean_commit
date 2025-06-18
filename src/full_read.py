from src.ssd import VirtualSSD
class FullRead:
    def __init__(self, ssd:VirtualSSD):
        self._ssd = ssd

    def run(self):
        for _ in range(self._ssd.LBA_COUNT):   # ssd.py에 100으로 정의 :contentReference[oaicite:0]{index=0}
            print(self._ssd.DEFAULT_VAL)
