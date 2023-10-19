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
class Task:
    title: str
    status: Status = Status.OPEN
    description: Optional[str] = None
    date_timestamp: Optional[datetime.date] = None
    start_timestamp: Optional[datetime.date] = None
    end_timestamp: Optional[datetime.date] = None
    goal: Optional[str] = None
