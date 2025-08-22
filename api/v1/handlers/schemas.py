from pydantic import BaseModel, Field
from pydantic import model_validator
from uuid import UUID

class CreateTaskInput(BaseModel):
    name: str = Field(..., title="Название", description="Короткое название задачи")
    description: str = Field(..., title="Описание", description="Подробное текстовое описание задачи")
    status: str = Field("created", title="Статус", description="Текущий статус задачи (по умолчанию created)")

class UpdateTaskInput(BaseModel):
    uuid: UUID
    name: str | None = None
    description: str | None = None
    status: str | None = None

    @model_validator(mode="after")
    def ensure_any_field(self):
        if not any([self.name, self.description, self.status]):
            raise ValueError("NO_FIELDS")
        return self

class DeleteTaskInput(BaseModel):
    uuid: UUID = Field(..., title="UUID задачи", description="Уникальный идентификатор удаляемой задачи")

class GetTaskOutput(BaseModel):
    uuid: UUID = Field(..., title="UUID задачи", description="Уникальный идентификатор задачи")
    name: str = Field(..., title="Название", description="Название задачи")
    description: str = Field(..., title="Описание", description="Подробное описание задачи")
    status: str = Field(..., title="Статус", description="Текущий статус задачи")

class GetTasksOutput(BaseModel):
    tasks: list[GetTaskOutput] = Field(..., title="Список задач", description="Массив объектов задач")

class CreateTaskOutput(BaseModel):
    uuid: UUID = Field(..., title="UUID задачи", description="Уникальный идентификатор созданной задачи")
    name: str = Field(..., title="Название", description="Название созданной задачи")
    description: str = Field(..., title="Описание", description="Описание созданной задачи")
    status: str = Field(..., title="Статус", description="Статус созданной задачи")

class UpdateTaskOutput(BaseModel):
    uuid: UUID = Field(..., title="UUID задачи", description="Уникальный идентификатор обновлённой задачи")
    name: str = Field(..., title="Название", description="Актуальное название задачи после обновления")
    description: str = Field(..., title="Описание", description="Актуальное описание задачи после обновления")
    status: str = Field(..., title="Статус", description="Актуальный статус задачи после обновления")

class DeleteTaskOutput(BaseModel):
    uuid: UUID = Field(..., title="UUID задачи", description="Идентификатор удалённой задачи")



