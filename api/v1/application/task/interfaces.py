from abc import abstractmethod  
from uuid import UUID
from typing import Protocol
from domen.entities import Task

class TaskGetter(Protocol):
    @abstractmethod
    def get(self, task_uuid: UUID) -> Task:
        """
        Получить по UUID.
        Исключения: нет (отсутствие -> None в реализации).
        """
        pass

class TasksGetter(Protocol):
    @abstractmethod
    def get_all(self) -> list[Task]:
        """
        Получить все.
        Исключения: нет.
        """
        pass

class TaskCreater(Protocol):
    @abstractmethod
    def create(self, task_data: Task) -> None:
        """
        Создать.
        Исключения:
          - TaskUniqueConstraintError (дубликат имени).
        """
        pass
    
class TaskUpdater(Protocol):
    @abstractmethod
    def update(self, task_data: dict) -> None:
        """
        Обновить.
        Исключения:
          - TaskNotFoundError (не существует).
          - TaskUniqueConstraintError (дубликат имени).
        """
        pass
    
class TaskDeleter(Protocol):
    @abstractmethod
    def delete(self, task_uuid: UUID) -> None:
        """
        Удалить.
        Исключения:
          - TaskNotFoundError (не существует).
        """
        pass