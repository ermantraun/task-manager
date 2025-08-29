import asyncio
import re
import pytest
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from config import Config
from dishka import make_async_container
from ioc import App  
from application.task import interactors, dto, exceptions
from domen.entities import TaskStatus

config = Config()


@pytest.fixture(scope="module")
def test_config():
    cfg = config
    cfg.postgres.database = "test_" + cfg.postgres.database
    return cfg

@pytest.fixture(scope="module")
async def container(test_config):
    provider = App() if callable(App) else App 
    c = make_async_container(provider, context={Config: test_config})
    yield c

@pytest.fixture(scope="function")
async def create_interactor(container):
    async with container() as request_scope:
        await request_scope.get(interactors.CreateTaskInteractor)



@pytest.fixture(scope='module', autouse=True)
async def clean_db(container):
    yield
    session: AsyncSession = await container.get(AsyncSession)
    await session.execute(sa.text("DELETE FROM tasks"))
    await session.commit()



_ALLOWED_STATUSES = ",".join(s.value for s in TaskStatus)

invalid_cases = [
    (" ", "Valid description", "created",
     exceptions.TaskValidationError, r"name: длина строки должна быть не меньше 1 символ"),
    ("a" * 101, "Valid description", "created",
     exceptions.TaskValidationError, r"name: длина строки должна быть не больше 100 символ"),
    ("Valid Name 1", " ", "created",
     exceptions.TaskValidationError, r"description: длина строки должна быть не меньше 1 символ"),
    ("Valid Name 2", "b" * 2001, "created",
     exceptions.TaskValidationError, r"description: длина строки должна быть не больше 2000 символ"),
    ("Valid Name 3", "Valid Description", "invalid_status",
     exceptions.TaskValidationError, rf"status: недопустимое значение \(allowed:{_ALLOWED_STATUSES}\)"),
]


@pytest.mark.anyio
@pytest.mark.parametrize("name,description,status,err,msg_regex", invalid_cases)
async def test_create_task_invalid(name, description, status, err, msg_regex, create_interactor):
    create_interactor = await create_interactor.execute(interactors.CreateTaskInteractor)
    with pytest.raises(err, match=msg_regex):
        await create_interactor(dto.CreateTaskInput(name=name, description=description, status=status))
