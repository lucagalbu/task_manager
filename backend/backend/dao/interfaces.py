from typing_extensions import TypedDict
import datetime
from enum import Enum
from typing import Optional, Protocol


class Status(Enum):
    DONE = 0
    PROGRESS = 1
    OPEN = 2


class TaskInput(TypedDict):
    title: str
    status: Status
    description: Optional[str]
    date: Optional[datetime.date]
    start_time: Optional[datetime.time]
    end_time: Optional[datetime.time]
    goal: Optional[str]


class TaskOutput(TaskInput):
    id: int


class DAO(Protocol):
    def getTaskByID(self, id: int) -> TaskOutput:
        ...

    def getAllTasks(self) -> list[TaskOutput]:
        ...

    def addTask(self, task: TaskInput) -> TaskOutput:
        ...

    def rmTask(self, id: int) -> TaskOutput:
        ...
