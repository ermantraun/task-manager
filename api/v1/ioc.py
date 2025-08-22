from dishka import Provider, provide, Scope, from_context, AnyOf
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from config import Config
from infrastructure.db.database import new_session_maker
from infrastructure.db import repositories
from typing import AsyncIterable
from application import common_interfaces
from application.task import interfaces as task_interfaces
from application.task import interactors

class FastApiApp(Provider):
    config = from_context(provides=Config, scope=Scope.APP)

    

    @provide(scope=Scope.APP)
    async def get_session_maker(self, config: Config) -> async_sessionmaker[AsyncSession]:
        async_session_maker = await new_session_maker(config.postgres)
        return async_session_maker
    
    @provide(scope=Scope.REQUEST)
    async def get_async_session(self, async_sessionmaker: async_sessionmaker[AsyncSession]) -> AsyncIterable[AnyOf[AsyncSession, common_interfaces.DBSession]]:
        async with async_sessionmaker() as session:
            yield session
    
    
    task_repository = provide(repositories.TaskRepository, scope=Scope.REQUEST, provides=AnyOf[task_interfaces.TaskCreater, task_interfaces.TaskGetter, task_interfaces.TasksGetter, task_interfaces.TaskUpdater, 
                              task_interfaces.TaskDeleter])
    
    get_task_interactor = provide(interactors.GetTaskInteractor, scope=Scope.REQUEST, provides=interactors.GetTaskInteractor)
    get_tasks_interactor = provide(interactors.GetTasksInteractor, scope=Scope.REQUEST, provides=interactors.GetTasksInteractor)
    create_task_interactor = provide(interactors.CreateTaskInteractor, scope=Scope.REQUEST, provides=interactors.CreateTaskInteractor)
    update_task_interactor = provide(interactors.UpdateTaskInteractor, scope=Scope.REQUEST, provides=interactors.UpdateTaskInteractor)
    delete_task_interactor = provide(interactors.DeleteTaskInteractor, scope=Scope.REQUEST, provides=interactors.DeleteTaskInteractor)