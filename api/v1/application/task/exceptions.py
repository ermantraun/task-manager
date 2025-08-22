class TaskError(Exception):
    pass

class TaskValidationError(TaskError):
    pass

class TaskNotFoundError(TaskError):
    pass

class TaskUniqueConstraintError(TaskError):
    pass
