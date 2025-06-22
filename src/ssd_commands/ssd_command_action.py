from src.ssd_file_manager import SSDFileManager
from src.command_buffer_handler import CommandBufferHandler
from abc import ABC, abstractmethod


class InvalidArgumentException(Exception):
    __module__ = 'builtins'


class SSDCommand(ABC):
    registry = {}

    def __init__(self, ssd_file_manager:SSDFileManager, command_buffer:CommandBufferHandler, *args):
        self._ssd_file_manager = ssd_file_manager
        self._command_buffer = command_buffer
        self._arguments = args

    @abstractmethod
    def run(self) -> str:
        ...

    @abstractmethod
    def validate(self) -> bool:
        ...
