from fastapi import APIRouter, status, Path, HTTPException
from typing import Annotated
from dishka.integrations.fastapi import FromDishka, DishkaRoute
from uuid import UUID
from dataclasses import asdict
from application.task import dto
from application.task import interactors
from . import schemas
from . import responses_descriptions as resp

router = APIRouter(prefix='/tasks', tags=['tasks'], route_class=DishkaRoute)



@router.get(
    '/{uuid}',
    status_code=status.HTTP_200_OK,
    description='Get task',
    responses=resp.GET_TASK_RESPONSES,
    response_model=schemas.GetTaskOutput,
)
async def get_task(
    uuid: Annotated[UUID, Path(title='UUID задачи')],
    interactor: FromDishka[interactors.GetTaskInteractor],
) -> dict:
    result = await interactor.execute(uuid)
    return asdict(result)

@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    description='Get all tasks',
    responses=resp.GET_TASKS_RESPONSES,
    response_model=schemas.GetTasksOutput,
)
async def get_tasks(
    interactor: FromDishka[interactors.GetTasksInteractor],
) -> dict:
    results = await interactor.execute()
    return {"tasks": [asdict(r) for r in results]}

@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    description='Create task',
    responses=resp.CREATE_TASK_RESPONSES,
    response_model=schemas.CreateTaskOutput,
)
async def create_task(
    data: schemas.CreateTaskInput,
    interactor: FromDishka[interactors.CreateTaskInteractor],
) -> dict:
    result = await interactor.execute(dto.CreateTaskInput(**data.model_dump()))
    return asdict(result)

@router.put(
    '/',
    status_code=status.HTTP_200_OK,
    description='Update task',
    responses=resp.UPDATE_TASK_RESPONSES,
    response_model=schemas.UpdateTaskOutput,
)
async def update_task(
    data: schemas.UpdateTaskInput,
    interactor: FromDishka[interactors.UpdateTaskInteractor],
) -> dict:

    result = await interactor.execute(dto.UpdateTaskInput(**data.model_dump()))
    return asdict(result)

@router.delete(
    '/{uuid}',
    status_code=status.HTTP_204_NO_CONTENT,
    description='Delete task',
    responses=resp.DELETE_TASK_RESPONSES,
)
async def delete_task(
    uuid: Annotated[UUID, Path(title='UUID удаленной задачи')],
    interactor: FromDishka[interactors.DeleteTaskInteractor],
) -> None:
    await interactor.execute(uuid)

