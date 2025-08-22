from domen.entities import Task
from ..common_interfaces import DBSession
from uuid import UUID
from . import interfaces
from . import dto
from . import exceptions

class GetTaskInteractor:
    def __init__(self, task_getter: interfaces.TaskGetter):
        self.task_getter = task_getter

    async def execute(self, uuid: UUID) -> dto.GetTaskOutput:
        task = await self.task_getter.get(uuid)
        if not task:
            raise exceptions.TaskNotFoundError("Task не найден")
        return task

class GetTasksInteractor:
    def __init__(self, tasks_getter: interfaces.TasksGetter):
        self.tasks_getter = tasks_getter

    async def execute(self) -> dto.GetTasksOutput:
        tasks = await self.tasks_getter.get_all()
        return tasks

class CreateTaskInteractor:
    def __init__(self, task_creater: interfaces.TaskCreater, session: DBSession):
        self.task_creater = task_creater
        self.session = session
        
    async def execute(self, data: dto.CreateTaskInput) -> dto.CreateTaskOutput:
        new_task = await self.task_creater.create(data)
        await self.session.commit()
        return new_task
    
class UpdateTaskInteractor:
    def __init__(self, task_updater: interfaces.TaskUpdater, session: DBSession):
        self.task_updater = task_updater
        self.session = session
        
    async def execute(self, data: dto.UpdateTaskInput) -> dto.UpdateTaskOutput:
        task = await self.task_updater.get(data.uuid)
        if not task:
            raise exceptions.TaskNotFoundError("Task не найден")
        fields = {k: v for k, v in data.__dict__.items() if k != "uuid" and v is not None}
        updated_task = await self.task_updater.update(task, fields)
        await self.session.commit()
        return updated_task

class DeleteTaskInteractor:
    def __init__(self, task_deleter: interfaces.TaskDeleter, session: DBSession):
        self.task_deleter = task_deleter
        self.session = session
        
    async def execute(self, uuid: UUID) -> UUID:
        await self.task_deleter.delete(uuid)
        await self.session.commit()
        return uuid
