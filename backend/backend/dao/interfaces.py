from typing_extensions import TypedDict
import datetime
from typing import Protocol

class OptionalFields(TypedDict, total=False):
    description: str
    date: datetime.date
    start_time: datetime.time
    end_time: datetime.time
    goal: str

class TaskInput(OptionalFields):
    title: str
    status: str

class TaskOutput(TaskInput):
    id: int

class TaskUpdate(OptionalFields, total=False):
    title: str
    status: str


class DAO(Protocol):
    def getTaskByID(self, id: int) -> TaskOutput:
        ...

    def getAllTasks(self) -> list[TaskOutput]:
        ...

    def addTask(self, task: TaskInput) -> TaskOutput:
        ...

    def rmTask(self, id: int) -> TaskOutput:
        ...

    def updateTask(self, id: int, new_fields: TaskUpdate) -> TaskOutput:
        ...
