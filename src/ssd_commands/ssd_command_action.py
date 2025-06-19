from abc import ABC, abstractmethod


class InvalidArgumentException(Exception):
    __module__ = 'builtins'


class SSDCommandAction(ABC):
    registry = {}

    def __init__(self, ssd_file_manager, *args):
        self._ssd_file_manager = ssd_file_manager
        self._arguments = args

    @abstractmethod
    def run(self) -> str:
        ...

    @abstractmethod
    def validate(self) -> bool:
        ...
