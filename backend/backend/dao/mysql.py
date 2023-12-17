"""Module that contains the DAO implementation based on MySQL"""

from datetime import datetime
import logging
from dataclasses import dataclass
from typing import cast
import mysql.connector
import mysql.connector.connection
import mysql.connector.cursor
from backend.dao.interfaces import TaskInput, TaskOutput, TaskUpdate


@dataclass
class MysqlConfig:
    """Configuration for the MySQL database."""

    password: str
    host: str = "localhost"
    user: str = "root"
    port: int = 3306
    database = "tasks"
    table = "tasks"


class Mysql:
    """Implementation of the DAO using MySQL as database."""

    _mydb: mysql.connector.connection.MySQLConnection
    _cursor: mysql.connector.cursor.MySQLCursorDict
    _config: MysqlConfig

    def __init__(self, config: MysqlConfig):
        self._config = config

        logging.info("Connecting to database")
        self.__connect()

        logging.info(f"Checking existence of tasks database '{self._config.database}'")
        database_exists = self.__checkDatabaseExists()

        if not database_exists:
            logging.info("Database not found. Creating it")
            self.__createTasksDatabase()
            if not self.__checkDatabaseExists():
                raise RuntimeError("Unable to create the database")
        else:
            logging.info("Database already existing")

        logging.info(f"Switching to database {self._config.database}")
        self.__switchToTaksDatabase()

        logging.info(f"Checking existence of tasks table '{self._config.table}'")
        table_exists = self.__checkTableExists()

        if not table_exists:
            logging.info("Table not found. Creating it")
            self.__createTasksTable()
            if not self.__checkTableExists():
                raise RuntimeError("Unable to create the table")
        else:
            logging.info("Table already existing")

    def __connect(self):
        # Use a pure Python connection. This is always available. Maybe less performant than the C
        # implementation, but I do not expect huge databases.
        connection = mysql.connector.connect(
            password=self._config.password,
            host=self._config.host,
            user=self._config.user,
            port=self._config.port,
            use_pure=True,
        )
        if isinstance(connection, mysql.connector.connection.MySQLConnection):
            self._mydb = connection
            self._cursor = cast(
                mysql.connector.cursor.MySQLCursorDict,
                self._mydb.cursor(dictionary=True),
            )
        else:
            raise mysql.connector.errors.DatabaseError(
                f"Expected a MySQLConnection connection, returned {type(connection)}"
            )

    def __createTasksDatabase(self):
        self._cursor.execute(f"CREATE DATABASE {self._config.database}")

    def __checkDatabaseExists(self):
        self._cursor.execute("SHOW DATABASES")
        databases = [
            result["Database"]
            for result in self._cursor.fetchall()
            if result is not None
        ]
        return self._config.database in databases

    def __switchToTaksDatabase(self):
        self._cursor.execute(f"USE {self._config.database};")

    # TODO: Use schema validation using the Task type
    # TODO: Can MySQL use enum for status?
    def __createTasksTable(self):
        id = "id INT AUTO_INCREMENT PRIMARY KEY"
        title = "title VARCHAR(255) NOT NULL"
        description = "description TEXT"
        date = "date TIMESTAMP"
        start_time = "start_time TIME"
        end_time = "end_time TIME"
        goal = "goal VARCHAR(255)"
        status = "status VARCHAR(50) NOT NULL"
        schema = ", ".join(
            [id, title, description, date, start_time, end_time, goal, status]
        )

        self._cursor.execute(f"CREATE TABLE {self._config.table} ({schema})")

    def __checkTableExists(self):
        self._cursor.execute("SHOW TABLES")
        tables = [
            result[f"Tables_in_{self._config.database}"]
            for result in self._cursor.fetchall()
            if result is not None
        ]
        return self._config.table in tables

    def __del__(self):
        logging.info("Closing database connection")
        self._mydb.close()

    def getTaskByID(self, id: int) -> TaskOutput:
        """Return a specific task from the database.
        Parameters
        ----------
        id: int
            Id of the task to be retrieved.
        """

        sql_command = f"SELECT  * FROM {self._config.table} WHERE id={id}"
        self._cursor.execute(sql_command)
        result = self._cursor.fetchall()

        if len(result) != 1:
            logging.warning(
                "Multiple tasks with the same id found. Using the first one"
            )

        task = TaskOutput(**result[0])  # type: ignore
        return task

    @staticmethod
    def convertSqlToTask(**fields) -> TaskOutput:
        """Convert a Task as stored in the database to the internal task representation.

        For example, it takes care to correctly convert the dates and times.

        Parameters
        ----------
        fields: dict
            Dictiornary containing the task data as returned by MySQL.
        """

        if "start_time" in fields:
            fields["start_time"] = (datetime.min + fields["start_time"]).time()
        if "end_time" in fields:
            fields["end_time"] = (datetime.min + fields["end_time"]).time()

        task = TaskOutput(**fields)
        return task

    def getAllTasks(self) -> list[TaskOutput]:
        """Return all the tasks in the database."""

        sql_command = f"SELECT  * FROM {self._config.table}"
        self._cursor.execute(sql_command)
        results = self._cursor.fetchall()

        tasks = [Mysql.convertSqlToTask(**arg) for arg in results if arg is not None]
        return tasks

    def addTask(self, task: TaskInput) -> TaskOutput:
        """Add a new task to the database and return it.

        Parameters
        ----------
        task: TypedDict (TaskInput)
            Dictionary containing the information about the new task.
            See the typed dictionary TaskInput for more details on the fields.
        """

        fields = []

        if task["title"] is not None:
            fields.append(("title", task["title"], "%s"))
        if task.get("description") is not None:
            fields.append(("description", task.get("description"), "%s"))
        if task.get("date") is not None:
            fields.append(("date", task.get("date"), "%s"))
        if task.get("start_time") is not None:
            fields.append(("start_time", task.get("start_time"), "%s"))
        if task.get("end_time") is not None:
            fields.append(("end_time", task.get("end_time"), "%s"))
        if task.get("goal") is not None:
            fields.append(("goal", task.get("goal"), "%s"))
        if task.get("status") is not None:
            fields.append(("status", task["status"], "%s"))

        columns = ", ".join([field[0] for field in fields])
        values = [field[1] for field in fields]
        values_types = ", ".join([field[2] for field in fields])

        sql_command = (
            f"INSERT INTO {self._config.table} ({columns}) VALUES ({values_types})"
        )

        self._cursor.execute(operation=sql_command, params=values)
        self._mydb.commit()

        id = self._cursor.getlastrowid()
        if id is None or self._cursor.rowcount != 1:
            raise RuntimeError("Unable to add key to the database")

        added_task = self.getTaskByID(id)
        return added_task

    def rmTask(self, id: int) -> TaskOutput:
        """Remove a task from the database and return it.

        Parameters
        ----------
        id: int
            Id of the task to be removed.
        """

        task = self.getTaskByID(id)
        # TODO: Check if task exists, otherwise do not proceed
        sql_command = f"DELETE FROM {self._config.table} WHERE id={task['id']}"
        self._cursor.execute(sql_command)
        self._mydb.commit()
        # TODO: Check that the task doesn't exist, i.e. it has been succesfully deleted
        return task

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

        # TODO: Check if task exists, otherwise check what happens

        fields = []

        if new_fields.get("title") is not None:
            fields.append(f"title='{new_fields.get('title')}'")
        if new_fields.get("description") is not None:
            fields.append(f"description='{new_fields.get('description')}'")
        if new_fields.get("date") is not None:
            fields.append(f"date='{new_fields.get('date')}'")
        if new_fields.get("start_time") is not None:
            fields.append(f"start_time='{new_fields.get('start_time')}'")
        if new_fields.get("end_time") is not None:
            fields.append(f"end_time='{new_fields.get('end_time')}'")
        if new_fields.get("goal") is not None:
            fields.append(f"goal='{new_fields.get('goal')}'")
        if new_fields.get("status") is not None:
            fields.append(f"status='{new_fields.get('status')}'")

        fields_str = ", ".join(fields)

        sql_command = f"""UPDATE {self._config.table}
        SET {fields_str}
        WHERE id={id};"""
        self._cursor.execute(sql_command)
        self._mydb.commit()

        task = self.getTaskByID(id)
        return task
