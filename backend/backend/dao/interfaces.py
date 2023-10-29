from dataclasses import dataclass
import datetime
from enum import Enum
from typing import Optional, Protocol


class Status(Enum):
    DONE = 0
    PROGRESS = 1
    OPEN = 2


@dataclass
class TaskInput:
    title: str
    status: Status
    description: Optional[str]
    date: Optional[datetime.date]
    start_time: Optional[datetime.date]
    end_time: Optional[datetime.date]
    goal: Optional[str]


@dataclass
class TaskOutput(TaskInput):
    id: int


class DAO(Protocol):
    def getTaskByID(self, id: int) -> TaskOutput:
        ...

    def getAllTasks(self) -> list[TaskOutput]:
        ...

    def addTask(self, task: TaskInput) -> TaskOutput:
        ...
