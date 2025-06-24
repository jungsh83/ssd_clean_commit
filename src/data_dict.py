"""공용 상수 모음"""
# ── 버퍼 상수 ───────────────────────────────────────────
LBA_START_INDEX: int = 0
LBA_COUNT: int = 100
DEFAULT_VAL: str = "0x00000000"
ERROR_TEXT: str = 'ERROR'
VALID_RETURN_CODE = 0
VALUE_LENGTH = 10
ERASE_SIZE_MIN = 0
ERASE_SIZE_MAX = 10
VALID_ARGUMENT_SINGLE: int = 1
VALID_ARGUMENT_RANGE: int = 2
INIT_VAL_INT: int = -1
INIT_VAL_STR: str = ""

# ── 커맨드 타입 ───────────────────────────────────────────
COMMAND_READ: str = "R"
COMMAND_WRITE: str = "W"
