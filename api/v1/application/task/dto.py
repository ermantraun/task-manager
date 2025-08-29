from dataclasses import dataclass
from uuid import UUID, uuid4
from domen import entities
from . import exceptions

ALLOWED_STATUSES = {s.value for s in entities.TaskStatus}

class TaskFieldChecker:
    @staticmethod
    def is_valid_status(status: str) -> list[str] | None:
        return [f"status: недопустимое значение (allowed: {','.join(ALLOWED_STATUSES)})"] if status not in ALLOWED_STATUSES else None
    
    @staticmethod
    def is_valid_name(name: str) -> list[str] | None:
        errors = []
        if not name or not name.strip():
            errors.append("name: пустое значение")
        if len(name) > 100:
            errors.append("name: длина > 100")
        return errors if errors else None
    
    @staticmethod
    def is_valid_description(description: str) -> list[str] | None:
        errors = []
        if not description or not description.strip():
            errors.append("description: пустое значение")
        if len(description) > 2000:
            errors.append("description: длина > 2000")
        return errors if errors else None

@dataclass
class GetTaskInput:
    uuid: UUID

@dataclass
class CreateTaskInput:
    name: str
    description: str
    status: str = "created"
    def validate(self):
        errors: list[str] = []
        if (e := TaskFieldChecker.is_valid_name(self.name)):
            errors.extend(e)
        if (e := TaskFieldChecker.is_valid_description(self.description)):
            errors.extend(e)
        if (e := TaskFieldChecker.is_valid_status(self.status)):
            errors.extend(e)
        if errors:
            raise exceptions.TaskValidationError("; ".join(errors))

@dataclass
class UpdateTaskInput:
    uuid: UUID
    name: str | None = None
    description: str | None = None
    status: str | None = None
    def validate(self):
        if self.name is None and self.description is None and self.status is None:
            raise exceptions.TaskValidationError("не передано ни одного поля для обновления")
        errors: list[str] = []
        if self.name is not None:
            if (e := TaskFieldChecker.is_valid_name(self.name)):
                errors.extend(e)
        if self.description is not None:
            if (e := TaskFieldChecker.is_valid_description(self.description)):
                errors.extend(e)
        if self.status is not None:
            if (e := TaskFieldChecker.is_valid_status(self.status)):
                errors.extend(e)
        if errors:
            raise exceptions.TaskValidationError("; ".join(errors))

@dataclass
class DeleteTaskInput:
    uuid: str

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

