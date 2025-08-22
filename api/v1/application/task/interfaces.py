from abc import abstractmethod  
from uuid import UUID
from typing import Protocol
from domen.entities import Task

class TaskGetter(Protocol):
    @abstractmethod
    def get(self, task_uuid: UUID) -> Task:
        pass

class TasksGetter(Protocol):
    @abstractmethod
    def get_all(self) -> list[Task]:
        pass

class TaskCreater(Protocol):
    @abstractmethod
    def create(self, task_data: Task) -> None:
        pass
    
class TaskUpdater(Protocol):
    @abstractmethod
    def update(self, task_data: dict) -> None:
        pass
    
    
class TaskDeleter(Protocol):
    @abstractmethod
    def delete(self, task_uuid: UUID) -> None:
        pass