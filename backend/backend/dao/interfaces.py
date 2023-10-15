from dataclasses import dataclass
import datetime
from enum import Enum
from typing import Optional, Protocol


class Status(Enum):
    DONE = 0
    PROGRESS = 1
    OPEN = 2


@dataclass
class Task:
    title: str
    status: Status = Status.OPEN
    description: Optional[str] = None
    date: Optional[datetime.date] = None
    start_time: Optional[datetime.date] = None
    end_time: Optional[datetime.date] = None
    goal: Optional[str] = None


class DAO(Protocol):
    def getTaskByID(self, id: int) -> Task:
        ...

    def addTask(self, task: Task) -> int:
        ...
