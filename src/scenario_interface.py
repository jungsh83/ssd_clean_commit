from abc import ABC, abstractmethod


class IScenarioTest(ABC):
    @abstractmethod
    def read_compare(self, addr: int, expected: str) -> bool:
        ...

    @abstractmethod
    def run_test(self) -> str:
        ...
