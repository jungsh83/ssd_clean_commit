from src.data_dict import LBA_START_INDEX, LBA_COUNT

def validate_lba(lba: str) -> bool:
    if not lba.isdigit():
        return False
    return LBA_START_INDEX <= int(lba) < LBA_COUNT

def validate_value(value: str) -> bool:
    if not isinstance(value, str) or len(value) != 10:
        return False
    if not value.startswith("0x"):
        return False
    hex_part = value[2:]
    return all(c in "0123456789ABCDEF" for c in hex_part)