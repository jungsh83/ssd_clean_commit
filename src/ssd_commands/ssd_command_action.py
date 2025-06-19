from abc import ABC, abstractmethod


class InvalidArgumentException(Exception):
    __module__ = 'builtins'


class SSDCommand(ABC):
    registry = {}

    def __init__(self, ssd_file_manager, *args):
        self._ssd_file_manager = ssd_file_manager
        self._arguments = args

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if hasattr(cls, 'command_name'):
            for name in cls.command_name:
                SSDCommand.registry[name] = cls

    @abstractmethod
    def run(self) -> str:
        ...

    @abstractmethod
    def validate(self) -> bool:
        ...
