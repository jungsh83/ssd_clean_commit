"""공용 상수 모음"""

# ── 버퍼 관련 ─────────────────────────────────────────────
VALID_ARGUMENT_LEN: int = 2
VALID_ARGUMENT_SINGLE: int = 1
VALID_ARGUMENT_RANGE: int = 2
INVALID_LBA: int = -1  # Erase Size 0일 경우, 사용
MAX_ERASE_LEN_ON_SSD_DRIVER: int = 10
LBA_START_INDEX: int = 0
LBA_COUNT: int = 100
DEFAULT_VAL: str = "0x00000000"
START_TEST_VALUE: int = 10000000
