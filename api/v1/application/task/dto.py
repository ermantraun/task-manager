from dataclasses import dataclass
from uuid import UUID, uuid4
from domen import entities
from . import exceptions

ALLOWED_STATUSES = {s.value for s in entities.TaskStatus}

@dataclass
class GetTaskInput:
    uuid: UUID

@dataclass
class CreateTaskInput:
    name: str
    description: str
    status: str = "created"
    def __post_init__(self):
        errors = []
        if not self.name or not self.name.strip():
            errors.append("name: пустое значение")
        if len(self.name) > 100:
            errors.append("name: длина > 100")
        if not self.description or not self.description.strip():
            errors.append("description: пустое значение")
        if self.status not in ALLOWED_STATUSES:
            errors.append(f"status: недопустимое значение (allowed: {','.join(ALLOWED_STATUSES)})")
        if errors:
            raise exceptions.TaskValidationError("; ".join(errors))

@dataclass
class UpdateTaskInput:
    uuid: UUID
    name: str | None = None
    description: str | None = None
    status: str | None = None
    def __post_init__(self):
        if self.name is None and self.description is None and self.status is None:
            raise exceptions.TaskValidationError("не передано ни одного поля для обновления")
        errors = []
        if self.name is not None:
            if not self.name.strip():
                errors.append("name: пустое значение")
            if len(self.name) > 100:
                errors.append("name: длина > 100")
        if self.description is not None and not self.description.strip():
            errors.append("description: пустое значение")
        if self.status is not None and self.status not in ALLOWED_STATUSES:
            errors.append(f"status: недопустимое значение (allowed: {','.join(ALLOWED_STATUSES)})")
        if errors:
            raise exceptions.TaskValidationError("; ".join(errors))

@dataclass
class DeleteTaskInput:
    uuid: str
    def __post_init__(self):
        try:
            UUID(str(self.uuid))
        except Exception:
            raise exceptions.TaskValidationError("uuid: неверный формат")

@dataclass
class GetTaskOutput:
    uuid: UUID
    name: str
    description: str
    status: str

@dataclass
class GetTasksOutput:
    tasks: list[entities.Task]

@dataclass
class CreateTaskOutput:
    uuid: UUID
    name: str
    description: str
    status: str

@dataclass
class UpdateTaskOutput:
    uuid: UUID
    name: str
    description: str
    status: str

@dataclass
class DeleteTaskOutput:
    uuid: UUID

