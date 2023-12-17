"""Module that contains the internal data formats used in this backend."""

from typing_extensions import TypedDict
import datetime
from typing import Protocol


class OptionalFields(TypedDict, total=False):
    """Optional fields that describe a task."""

    description: str
    date: datetime.date
    start_time: datetime.time
    end_time: datetime.time
    goal: str


class TaskInput(OptionalFields):
    """Task format as received from the outside world."""

    title: str
    status: str


class TaskOutput(TaskInput):
    """Task format as sent to the outside world."""

    id: int


class TaskUpdate(OptionalFields, total=False):
    """Fields that can be updated in a task.
    The API mutation parameters used to update the fields of a task are casted to this format.
    """

    title: str
    status: str


class DAO(Protocol):
    """Protocol specifying the methods that a DAO must provide."""


    def getTaskByID(self, id: int) -> TaskOutput:
        """Return a specific task from the database.
        Parameters
        ----------
        id: int
            Id of the task to be retrieved.
        """
        ...

    def getAllTasks(self) -> list[TaskOutput]:
        """Return all the tasks in the database."""
        ...

    def addTask(self, task: TaskInput) -> TaskOutput:
        """Add a new task to the database and return it.

        Parameters
        ----------
        task: TypedDict (TaskInput)
            Dictionary containing the information about the new task.
            See the typed dictionary TaskInput for more details on the fields.
        """
        ...

    def rmTask(self, id: int) -> TaskOutput:
        """Remove a task from the database and return it.

        Parameters
        ----------
        id: int
            Id of the task to be removed.
        """
        ...

    def updateTask(self, id: int, new_fields: TaskUpdate) -> TaskOutput:
        """Update a task in the database and return the updated task.

        Parameters
        ----------
        id: int
            Id of the task to be updated.
        new_fields: TypedDict (TaskUpdate)
            Dictionary with the fields to be updated. All and only the fields in the
            dictionary are updated. See the typed dictionary TaskUpdate for more details on
            the fields.
        """
        ...
