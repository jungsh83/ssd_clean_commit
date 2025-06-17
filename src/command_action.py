from abc import ABC, abstractmethod


class CommandAction(ABC):
    def __init__(self, ssd_driver, *args):
        self._ssd_driver = ssd_driver
        self._arguments = args

        self.validate()

    @abstractmethod
    def run(self) -> None:
        ...

    def validate(self) -> bool:
        ...
