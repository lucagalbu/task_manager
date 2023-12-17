"""GraphQL queries and mutations"""

import datetime
from typing import Optional
import strawberry
from strawberry.fastapi import GraphQLRouter
from backend.dao.interfaces import DAO
from backend.services.converters import (
    convertTaskDaoToGraphQL,
    convertTaskGraphqlToDao,
    convertTaskUpdateGraphQLToDao,
)
from backend.services.schemas import Status, TaskInput, TaskOutput, TaskUpdate


def get_task_by_id(dao: DAO, task_id: strawberry.ID) -> TaskOutput:
    """Asks the DAO to return a task with a specific ID.

    Parameters
    ----------
    dao: class (DAO)
        Data Access Object (DAO). See the DAO protocol for more information.
    task_id: int
        Id of the task to be retrieved.
    """

    task_dao = dao.get_task_by_id(int(task_id))
    task_ql = convertTaskDaoToGraphQL(task_dao)
    return task_ql


def get_all_tasks(dao: DAO) -> list[TaskOutput]:
    """Asks the DAO to return all tasks stored in the database.

    Parameters
    ----------
    dao: class (DAO)
        Data Access Object (DAO). See the DAO protocol for more information.
    """

    tasks_dao = dao.get_all_tasks()
    tasks_ql = [convertTaskDaoToGraphQL(task) for task in tasks_dao]
    return tasks_ql


def create_graphql_app(dao: DAO):
    """Factory function to create a GraphQL application.

    Parameters
    ----------
    dao: class (DAO)
        Data Access Object (DAO). See the DAO protocol for more information.
    """

    def get_tasks(task_id: Optional[strawberry.ID] = None) -> list[TaskOutput]:
        """Query to return tasks from the database.

        Parameters
        ----------
        task_id: int
            Id of the task to be retrieved. If None, all tasks are retrieved.
        """

        tasks: list[TaskOutput] = []
        if task_id is not None:
            tasks = [get_task_by_id(dao, task_id)]
        else:
            tasks = get_all_tasks(dao)

        return tasks

    # TODO: start and end times are not timestamp anymore
    def add_task(
        title: str,
        description: Optional[str] = None,
        date_timestamp: Optional[datetime.date] = None,
        start_timestamp: Optional[str] = None,
        end_timestamp: Optional[str] = None,
        goal: Optional[str] = None,
        status: Status = Status.OPEN,
    ) -> TaskOutput:
        """Mutation to add a new task to the database.

        Parameters
        ----------
        title: str
            Title of the task.
        description: str
            Description of the task (optional).
        date_timestamp: datetime.date
            Date the task must be worked on (optional).
        start_timestamp: str (hh:mm or hh:mm:ss)
            Start time when the task must be worked on (optional).
        end_timestamp: str (hh:mm or hh:mm:ss)
            End time when the task must be worked on (optional).
        goal: str
            Category, or goal, the task belongs to (optional).
        status: Status
            Status of the task (e.g., open, in progress,...).
            See the enumeration Status for the possible values.
        """

        start_time = (
            datetime.datetime.strptime(start_timestamp, "%H:%M").time()
            if start_timestamp
            else None
        )
        end_time = (
            datetime.datetime.strptime(end_timestamp, "%H:%M").time()
            if end_timestamp
            else None
        )

        task_ql = TaskInput(
            title=title,
            description=description,
            date_timestamp=date_timestamp,
            start_timestamp=start_time,
            end_timestamp=end_time,
            goal=goal,
            status=status,
        )
        task_dao = convertTaskGraphqlToDao(task_ql)
        added_task = dao.add_task(task_dao)
        return convertTaskDaoToGraphQL(added_task)

    def rm_task(task_id: int) -> TaskOutput:
        """Mutation to remove a task to the database. It returns the deleted task.

        Parameters
        ----------
        task_id: int
            Id of the task to be removed.
        """

        removed_id = dao.rm_task(task_id=task_id)
        return convertTaskDaoToGraphQL(removed_id)

    def update_task(
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        date_timestamp: Optional[float] = None,
        start_timestamp: Optional[str] = None,
        end_timestamp: Optional[str] = None,
        goal: Optional[str] = None,
        status: Optional[Status] = None,
    ) -> TaskOutput:
        """Mutation to update an existing task. It returns the updated task.

        Parameters that are None, or not given, correspond to the fields that
        are not updated.

        Parameters
        ----------
        task_id: int
            Id of the task to be updated.
        title: str
            Optional, new title of the task.
        description: str
            Optional, new description of the task.
        date_timestamp: datetime.date
            Optional, new date the task must be worked on.
        start_timestamp: str (hh:mm or hh:mm:ss)
            Optional, new start time when the task must be worked on.
        end_timestamp: str (hh:mm or hh:mm:ss)
            Optional, new end time when the task must be worked on.
        goal: str
            Optional, new category, or goal, the task belongs to.
        status: Status
            Optional, new status of the task (e.g., open, in progress,...).
            See the enumeration Status for the possible values.
        """

        date = datetime.date.fromtimestamp(date_timestamp) if date_timestamp else None
        start_time = (
            datetime.datetime.strptime(start_timestamp, "%H:%M").time()
            if start_timestamp
            else None
        )
        end_time = (
            datetime.datetime.strptime(end_timestamp, "%H:%M").time()
            if end_timestamp
            else None
        )

        task_ql = TaskUpdate(
            title=title,
            description=description,
            date_timestamp=date,
            start_timestamp=start_time,
            end_timestamp=end_time,
            goal=goal,
            status=status,
        )

        task_dao = convertTaskUpdateGraphQLToDao(task_ql=task_ql)
        task_updated = dao.update_task(task_id=task_id, new_fields=task_dao)
        return convertTaskDaoToGraphQL(task_updated)

    @strawberry.type
    class Query:
        """Class to specify the possible queries."""

        query_task: list[TaskOutput] = strawberry.field(
            resolver=get_tasks, description="Retrieve a list of tasks"
        )

    @strawberry.type
    class Mutation:
        """Class to specify the possible mutations."""

        add: TaskOutput = strawberry.field(
            resolver=add_task, description="Add one task to the database"
        )

        rm: TaskOutput = strawberry.field(
            resolver=rm_task, description="Remove one task from the database"
        )

        update: TaskOutput = strawberry.field(
            resolver=update_task, description="Update an existing task"
        )

    schema = strawberry.Schema(query=Query, mutation=Mutation)
    graphql_app = GraphQLRouter(schema)

    return graphql_app
