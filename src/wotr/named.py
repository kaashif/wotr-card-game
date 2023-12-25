from abc import ABC, abstractmethod


class Named(ABC):
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError()
