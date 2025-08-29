import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from application.task import interfaces
from application.task import dto
from application.task import exceptions
from domen import entities
from . import models
from uuid import UUID  

class TaskRepository(interfaces.TaskCreater, interfaces.TaskGetter, interfaces.TasksGetter, 
                     interfaces.TaskUpdater, interfaces.TaskDeleter):
    def __init__(self, session: AsyncSession) -> None:
        self.session: AsyncSession = session

    async def create(self, task_data: dto.CreateTaskInput) -> entities.Task:
        new_task = models.Task(**task_data.__dict__)
        self.session.add(new_task)
        try:
            await self.session.flush()
        except IntegrityError as e:
            raise exceptions.TaskUniqueConstraintError("task.name уже существует") from e
        return entities.Task(
            uuid=new_task.uuid,
            name=new_task.name,
            description=new_task.description,
            status=new_task.status
        )

    async def get(self, uuid: UUID) -> entities.Task | None:
        orm_task = await self.session.get(models.Task, uuid)
        if orm_task:
            return entities.Task(
                uuid=orm_task.uuid,
                name=orm_task.name,
                description=orm_task.description,
                status=orm_task.status
            )
        return None

    async def get_all(self) -> list[entities.Task]:
        result = await self.session.execute(sqlalchemy.select(models.Task))
        orm_tasks = result.scalars().all()
        return [
            entities.Task(
                uuid=task.uuid,
                name=task.name,
                description=task.description,
                status=task.status
            ) for task in orm_tasks
        ]
    
    async def update(self, task_data: dto.UpdateTaskInput) -> entities.Task:
        task = await self.get(task_data.uuid)
        if not task:
            raise exceptions.TaskNotFoundError("Task не найден")
        
        orm_task = await self.session.get(models.Task, task_data.uuid)
        for key, value in task_data.__dict__.items():
            if key == "uuid" or value is None:
                continue
            setattr(orm_task, key, value)
        
        try:
            await self.session.flush()
        except IntegrityError as e:
            raise exceptions.TaskUniqueConstraintError("task.name уже существует") from e
        
        return entities.Task(
            uuid=orm_task.uuid,
            name=orm_task.name,
            description=orm_task.description,
            status=orm_task.status
        )


    async def delete(self, uuid: UUID) -> None:
        orm_task = await self.session.get(models.Task, uuid)
        if not orm_task:
            raise exceptions.TaskNotFoundError("Task не найден")
        
        await self.session.delete(orm_task)