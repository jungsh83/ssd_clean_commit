from functools import cached_property
from abc import ABC, abstractmethod


class CommandAction(ABC):
    registry = {}

    def __init__(self, ssd_driver, *args):
        self._ssd_driver = ssd_driver
        self._arguments = args

    def __init_subclass__(cls):
        super().__init_subclass__()
        if hasattr(cls, 'command_name'):
            for command in cls.command_name:
                CommandAction.registry[command] = cls

    @abstractmethod
    def run(self) -> None:
        ...

    @abstractmethod
    def validate(self) -> bool:
        ...
