from typing_extensions import TypedDict
import datetime
from enum import Enum
from typing import Protocol


class Status(Enum):
    DONE = 0
    PROGRESS = 1
    OPEN = 2


class OptionalFields(TypedDict, total=False):
    description: str
    date: datetime.date
    start_time: datetime.date
    end_time: datetime.date
    goal: str

class TaskInput(OptionalFields):
    title: str
    status: Status

class TaskOutput(TaskInput):
    id: int

class TaskUpdate(OptionalFields, total=False):
    title: str
    status: Status


class DAO(Protocol):
    def getTaskByID(self, id: int) -> TaskOutput:
        ...

    def getAllTasks(self) -> list[TaskOutput]:
        ...

    def addTask(self, task: TaskInput) -> TaskOutput:
        ...

    def rmTask(self, id: int) -> TaskOutput:
        ...
