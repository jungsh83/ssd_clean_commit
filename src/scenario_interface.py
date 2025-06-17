from abc import ABC, abstractmethod


class IScenarioTest(ABC):
    def __init__(self, ssd_driver):
        self._ssd_driver = ssd_driver

    @abstractmethod
    def read_compare(self, addr: int, expected: str) -> bool:
        ...

    @abstractmethod
    def run_test(self) -> str:
        ...
