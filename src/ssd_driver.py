class ReadException(Exception):
    pass

class WriteException(Exception):
    pass

class SSDDriver:
    def __init__(self):
        pass

    def read(self, lba: int) -> str:
        """
        system call 날려도 되고, subprocess를 날려서 돌려도 됩니다.
        별개의 프로세스로 돌아가게 만든다.
        :param lba: 주소
        :return: 데이터
        :raise 'ERROR" return 받으면 ReadException 처리
        """
        return "0x00000000"

    def write(self, lba: int, value: str) -> None:
        """
        system call 날려도 되고, subprocess를 날려서 돌려도 됩니다.
        별개의 프로세스로 돌아가게 만든다.
        :param lba:
        :param value:
        :raise 'ERROR" return 받으면 WriteException 처리
        """
        pass