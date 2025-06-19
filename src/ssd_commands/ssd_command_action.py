from abc import ABC, abstractmethod


class InvalidArgumentException(Exception):
    __module__ = 'builtins'


class SSDCommand(ABC):
    registry = {}

    def __init__(self, ssd_file_manager, command_buffer, *args):
        self._ssd_file_manager = ssd_file_manager
        self._command_buffer = command_buffer
        self._arguments = args

    @abstractmethod
    def run(self) -> str:
        ...

    @abstractmethod
    def validate(self) -> bool:
        ...
