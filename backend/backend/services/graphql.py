import datetime
from typing import Optional
import strawberry
from strawberry.fastapi import GraphQLRouter
from backend.dao.interfaces import DAO
from backend.services.converters import convertTaskDaoToGraphQL, convertTaskGraphqlToDao, convertTaskUpdateGraphQLToDao
from backend.services.schemas import Status, TaskInput, TaskOutput, TaskUpdate


def getTaskByID(dao: DAO, id: strawberry.ID) -> TaskOutput:
    taskDao = dao.getTaskByID(int(id))
    taskQL = convertTaskDaoToGraphQL(taskDao)
    return taskQL


def getAllTasks(dao: DAO) -> list[TaskOutput]:
    tasksDao = dao.getAllTasks()
    tasksQL = [convertTaskDaoToGraphQL(task) for task in tasksDao]
    return tasksQL


def createGraphqlApp(dao: DAO):
    def getTasks(id: Optional[strawberry.ID] = None) -> list[TaskOutput]:
        tasks: list[TaskOutput] = []
        if id is not None:
            tasks = [getTaskByID(dao, id)]
        else:
            tasks = getAllTasks(dao)

        return tasks

    def addTask(
        title: str,
        description: Optional[str] = None,
        date_timestamp: Optional[datetime.date] = None,
        start_timestamp: Optional[datetime.time] = None,
        end_timestamp: Optional[datetime.time] = None,
        goal: Optional[str] = None,
        status: Status = Status.OPEN,
    ) -> TaskOutput:
        task_ql = TaskInput(
            title=title,
            description=description,
            date_timestamp=date_timestamp,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
            goal=goal,
            status=status,
        )
        task_dao = convertTaskGraphqlToDao(task_ql)
        added_task = dao.addTask(task_dao)
        return convertTaskDaoToGraphQL(added_task)

    def rmTask(id: int) -> TaskOutput:
        removed_id = dao.rmTask(id=id)
        return convertTaskDaoToGraphQL(removed_id)
    
    def updateTask(
            id: int,
            title: Optional[str] = None,
            description: Optional[str] = None,
            date_timestamp: Optional[float] = None,
            start_timestamp: Optional[float] = None,
            end_timestamp: Optional[float] = None,
            goal: Optional[str] = None,
            status: Optional[Status] = None
    ) -> TaskOutput:
        date = datetime.date.fromtimestamp(date_timestamp) if date_timestamp else None
        start_time = (
            datetime.date.fromtimestamp(start_timestamp) if start_timestamp else None
        )
        end_time = datetime.date.fromtimestamp(end_timestamp) if end_timestamp else None
        
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
        task_updated = dao.updateTask(id=id, new_fields=task_dao)
        return convertTaskDaoToGraphQL(task_updated)


    @strawberry.type
    class Query:
        query_task: list[TaskOutput] = strawberry.field(
            resolver=getTasks, description="Retrieve a list of tasks"
        )

    @strawberry.type
    class Mutation:
        add_task: TaskOutput = strawberry.field(
            resolver=addTask, description="Add one task to the database"
        )

        rm_task: TaskOutput = strawberry.field(
            resolver=rmTask, description="Remove one task from the database"
        )

        update_task: TaskOutput = strawberry.field(
            resolver=updateTask, description="Update an existing task"
        )

    schema = strawberry.Schema(query=Query, mutation=Mutation)
    graphql_app = GraphQLRouter(schema)

    return graphql_app
