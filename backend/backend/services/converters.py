from backend.dao.interfaces import Task as TaskDao, Status as StatusDao
from backend.services.schemas import Task as TaskQL, Status as StatusQL


def convertStatusDaoToGraphQL(status_dao: StatusDao) -> StatusQL:
    if status_dao == StatusDao.DONE:
        return StatusQL.DONE
    elif status_dao == StatusDao.OPEN:
        return StatusQL.OPEN
    if status_dao == StatusDao.PROGRESS:
        return StatusQL.PROGRESS
    else:
        return StatusQL.PROGRESS


def convertStatusGraphQLToDao(status_ql: StatusQL) -> StatusDao:
    if status_ql == StatusQL.DONE:
        return StatusDao.DONE
    elif status_ql == StatusQL.OPEN:
        return StatusDao.OPEN
    if status_ql == StatusQL.PROGRESS:
        return StatusDao.PROGRESS
    else:
        return StatusDao.PROGRESS


def convertTaskDaoToGraphQL(task_dao: TaskDao) -> TaskQL:
    status: StatusQL = convertStatusDaoToGraphQL(task_dao.status)

    return TaskQL(
        title=task_dao.title,
        description=task_dao.description,
        date_timestamp=task_dao.date,
        start_timestamp=task_dao.start_time,
        end_timestamp=task_dao.end_time,
        goal=task_dao.goal,
        status=status,
    )


def convertTaskGraphqlToDao(task_ql: TaskQL) -> TaskDao:
    status: StatusDao = convertStatusGraphQLToDao(task_ql.status)

    return TaskDao(
        title=task_ql.title,
        description=task_ql.description,
        date=task_ql.date_timestamp,
        start_time=task_ql.start_timestamp,
        end_time=task_ql.end_timestamp,
        goal=task_ql.goal,
        status=status,
    )
