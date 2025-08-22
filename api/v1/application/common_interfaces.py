from abc import abstractmethod  
from typing import Protocol


class DBSession(Protocol):
    @abstractmethod
    def commit(self) -> None:
        pass