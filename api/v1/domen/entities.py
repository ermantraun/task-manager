from dataclasses import dataclass
from enum import Enum
from uuid import UUID
class TaskStatus(Enum):
    CREATED = "created"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


@dataclass
class Task:
    uuid: UUID
    name: str
    description: str
    status: TaskStatus
    
    