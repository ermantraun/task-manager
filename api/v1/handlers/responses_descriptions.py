from . import schemas

GET_TASK_RESPONSES = {
    200: {
        "model": schemas.GetTaskOutput,
        "description": "Задача успешно получена"
    },
    404: {
        "description": "Задача не найдена",
        "content": {
            "application/json": {
                "example": {"error": "not_found", "detail": "Task не найден"}
            }
        },
    },
    422: {
        "description": "Ошибка валидации UUID",
        "content": {
            "application/json": {
                "example": {"error": "validation_error", "detail": "uuid: неверный формат"}
            }
        },
    },
}

GET_TASKS_RESPONSES = {
    200: {
        "model": schemas.GetTasksOutput,
        "description": "Список задач успешно получен"
    }
}

CREATE_TASK_RESPONSES = {
    201: {
        "model": schemas.CreateTaskOutput,
        "description": "Задача успешно создана"
    },
    409: {
        "description": "Нарушение уникальности (имя уже существует)",
        "content": {
            "application/json": {
                "example": {"error": "unique_violation", "detail": "task.name уже существует"}
            }
        },
    },
    422: {
        "description": "Ошибка валидации входных данных",
        "content": {
            "application/json": {
                "example": {"error": "validation_error", "detail": "name: пустое значение; description: пустое значение"}
            }
        },
    },
}

UPDATE_TASK_RESPONSES = {
    200: {
        "model": schemas.UpdateTaskOutput,
        "description": "Задача успешно обновлена"
    },
    404: {
        "description": "Задача для обновления не найдена",
        "content": {
            "application/json": {
                "example": {"error": "not_found", "detail": "Task не найден"}
            }
        },
    },
    409: {
        "description": "Нарушение уникальности при обновлении",
        "content": {
            "application/json": {
                "example": {"error": "unique_violation", "detail": "task.name уже существует"}
            }
        },
    },
    422: {
        "description": "Ошибка валидации входных данных (нет полей или формат)",
        "content": {
            "application/json": {
                "example": {"error": "validation_error", "detail": "не передано ни одного поля для обновления"}
            }
        },
    },
}

DELETE_TASK_RESPONSES = {
    200: {
        "description": "Задача успешно удалена (тело отсутствует)"
    },
    404: {
        "description": "Задача для удаления не найдена",
        "content": {
            "application/json": {
                "example": {"error": "not_found", "detail": "Task не найден"}
            }
        },
    },
    422: {
        "description": "Ошибка валидации UUID при удалении",
        "content": {
            "application/json": {
                "example": {"error": "validation_error", "detail": "uuid: неверный формат"}
            }
        },
    },
}
