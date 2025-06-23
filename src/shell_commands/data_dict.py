"""공용 상수 모음"""

# ── 버퍼 관련 ─────────────────────────────────────────────
VALID_ARGUMENT_LEN: int = 2
VALID_ARGUMENT_SINGLE: int = 1
VALID_ARGUMENT_RANGE: int = 2
INVALID_LBA: int = -1  # Erase Size 0일 경우, 사용
MAX_ERASE_LEN_ON_SSD_DRIVER: int = 10
LBA_START_INDEX = 0
LBA_COUNT = 100
DEFAULT_VAL = "0x00000000"