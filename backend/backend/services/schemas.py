"""Module with the data formats used by the API"""

import datetime
from enum import Enum
from typing import Optional
import strawberry


@strawberry.enum
class Status(Enum):
    """Possible values for the state of a task."""

    DONE = 0
    PROGRESS = 1
    OPEN = 2


@strawberry.type
class OptionalFields:
    """Optional fields describing a task in an API call."""

    description: Optional[str] = None
    date_timestamp: Optional[datetime.date] = None
    start_timestamp: Optional[datetime.time] = None
    end_timestamp: Optional[datetime.time] = None
    goal: Optional[str] = None


@strawberry.type
class TaskInput(OptionalFields):
    """Task fields as received from the outisde world."""

    title: str
    status: Status = Status.OPEN


@strawberry.type
class TaskOutput(TaskInput):
    """Task fields as outputted to the outside world."""

    id: int


@strawberry.type
class TaskUpdate(OptionalFields):
    """Task fields that can be updated."""

    title: Optional[str]
    status: Optional[Status]
