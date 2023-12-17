import datetime
from enum import Enum
from typing import Optional
import strawberry


@strawberry.enum
class Status(Enum):
    DONE = 0
    PROGRESS = 1
    OPEN = 2


@strawberry.type
class OptionalFields:
    description: Optional[str] = None
    date_timestamp: Optional[datetime.date] = None
    start_timestamp: Optional[datetime.time] = None
    end_timestamp: Optional[datetime.time] = None
    goal: Optional[str] = None


@strawberry.type
class TaskInput(OptionalFields):
    title: str
    status: Status = Status.OPEN


@strawberry.type
class TaskOutput(TaskInput):
    id: int


@strawberry.type
class TaskUpdate(OptionalFields):
    title: Optional[str]
    status: Optional[Status]
