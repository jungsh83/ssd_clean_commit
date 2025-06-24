from src.data_dict import LBA_START_INDEX, LBA_COUNT, VALUE_LENGTH, ERASE_SIZE_MIN, ERASE_SIZE_MAX


def validate_lba(lba: str) -> bool:
    if not str(lba).isdigit():
        return False
    return LBA_START_INDEX <= int(lba) < LBA_COUNT


def validate_value(value: str) -> bool:
    if not isinstance(value, str) or len(value) != VALUE_LENGTH:
        return False
    if not value.startswith("0x"):
        return False
    return all(c in "0123456789ABCDEF" for c in (value[2:]))


def validate_erase_size(lba: str, size: str) -> bool:
    if not validate_lba(lba) or not size.isdigit():
        return False

    return (
            ERASE_SIZE_MIN <= int(size) <= ERASE_SIZE_MAX and
            int(lba) + int(size) <= LBA_COUNT
    )
