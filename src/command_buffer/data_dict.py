"""공용 상수 모음"""

# ── 버퍼 관련 ─────────────────────────────────────────────
MAX_SIZE_OF_COMMAND_BUFFERS: int = 5
WRITE_SIZE: int = 1
ERASE_CHUNK_SIZE: int = 10
ERASE_VALUE: str = "0x00000000"

# ── 커맨드 타입 ───────────────────────────────────────────
ERASE: str = "E"
WRITE: str = "W"
EMPTY: str = "empty"
