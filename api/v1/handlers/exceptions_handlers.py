from fastapi import Request
from fastapi.responses import JSONResponse
from application.task import exceptions as task_exceptions

def task_validation_error_handler(request: Request, exc: task_exceptions.TaskValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": "validation_error",
            "detail": str(exc),
        },
    )

def task_not_found_error_handler(request: Request, exc: task_exceptions.TaskNotFoundError):
    return JSONResponse(
        status_code=404,
        content={
            "error": "not_found",
            "detail": str(exc),
        },
    )

def task_unique_error_handler(request: Request, exc: task_exceptions.TaskUniqueConstraintError):
    return JSONResponse(
        status_code=409,
        content={
            "error": "unique_violation",
            "detail": str(exc),
        },
    )

all_handlers = {
    task_exceptions.TaskValidationError: task_validation_error_handler,
    task_exceptions.TaskNotFoundError: task_not_found_error_handler,
    task_exceptions.TaskUniqueConstraintError: task_unique_error_handler,
}
