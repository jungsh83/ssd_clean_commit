from functools import cached_property
from abc import ABC, abstractmethod

from src.ssd import VirtualSSD


class CommandAction(ABC):
    def __init__(self, ssd_driver: VirtualSSD, *args):
        self._ssd_driver = ssd_driver
        self._arguments = args

    @abstractmethod
    def run(self) -> None:
        ...

    @abstractmethod
    def validate(self) -> bool:
        ...
