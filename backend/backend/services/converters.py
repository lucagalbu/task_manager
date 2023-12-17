""""Module with converters between the DAO and the API data formats"""

from backend.dao.interfaces import (
    TaskInput as TaskInDao,
    TaskUpdate as TaskUpdateDao,
    TaskOutput as TaskOutDao,
)
from backend.services.schemas import (
    TaskOutput as TaskOutQL,
    TaskInput as TaskInQL,
    TaskUpdate as TaskUpdateQL,
    Status as StatusQL,
)


def convertStatusDaoToGraphQL(status_dao: str) -> StatusQL:
    if status_dao == "DONE":
        return StatusQL.DONE
    elif status_dao == "OPEN":
        return StatusQL.OPEN
    if status_dao == "PROGRESS":
        return StatusQL.PROGRESS
    else:
        return StatusQL.PROGRESS


def convertStatusGraphQLToDao(status_ql: StatusQL) -> str:
    if status_ql == StatusQL.DONE:
        return "DONE"
    elif status_ql == StatusQL.OPEN:
        return "OPEN"
    if status_ql == StatusQL.PROGRESS:
        return "PROGRESS"
    else:
        return "PROGRESS"


def convertTaskUpdateGraphQLToDao(task_ql: TaskUpdateQL) -> TaskUpdateDao:
    status_dao = (
        convertStatusGraphQLToDao(task_ql.status)
        if task_ql.status is not None
        else None
    )

    task_dao: TaskUpdateDao = {}

    if status_dao is not None:
        task_dao["status"] = status_dao
    if task_ql.title is not None:
        task_dao["title"] = task_ql.title
    if task_ql.description is not None:
        task_dao["description"] = task_ql.description
    if task_ql.date_timestamp is not None:
        task_dao["date"] = task_ql.date_timestamp
    if task_ql.start_timestamp is not None:
        task_dao["start_time"] = task_ql.start_timestamp
    if task_ql.end_timestamp is not None:
        task_dao["end_time"] = task_ql.end_timestamp
    if task_ql.goal is not None:
        task_dao["goal"] = task_ql.goal

    return task_dao


def convertTaskDaoToGraphQL(task_dao: TaskOutDao) -> TaskOutQL:
    status: StatusQL = convertStatusDaoToGraphQL(task_dao["status"])

    return TaskOutQL(
        id=task_dao["id"],
        title=task_dao["title"],
        description=task_dao.get("description"),
        date_timestamp=task_dao.get("date"),
        start_timestamp=task_dao.get("start_time"),
        end_timestamp=task_dao.get("end_time"),
        goal=task_dao.get("goal"),
        status=status,
    )


def convertTaskGraphqlToDao(task_ql: TaskInQL) -> TaskInDao:
    status: str = convertStatusGraphQLToDao(task_ql.status)

    task_dao = TaskInDao(title=task_ql.title, status=status)

    if task_ql.description is not None:
        task_dao["description"] = task_ql.description
    if task_ql.date_timestamp is not None:
        task_dao["date"] = task_ql.date_timestamp
    if task_ql.start_timestamp is not None:
        task_dao["start_time"] = task_ql.start_timestamp
    if task_ql.end_timestamp is not None:
        task_dao["end_time"] = task_ql.end_timestamp
    if task_ql.goal is not None:
        task_dao["goal"] = task_ql.goal

    return task_dao
