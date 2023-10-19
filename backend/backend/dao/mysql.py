import dataclasses
import logging
import mysql.connector
import mysql.connector.connection
import mysql.connector.cursor
from dataclasses import dataclass
from backend.dao.interfaces import Task


@dataclass
class MysqlConfig:
    password: str
    host: str = "localhost"
    user: str = "root"
    port: int = 3306
    database = "tasks"
    table = "tasks"


class Mysql:
    _mydb: mysql.connector.connection.MySQLConnection
    _cursor: mysql.connector.cursor.MySQLCursor
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

        logging.info(f"Switching to database ${self._config.database}")
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
            self._cursor = self._mydb.cursor()
        else:
            raise mysql.connector.errors.DatabaseError(
                f"Expected a MySQLConnection connection, returned {type(connection)}"
            )

    def __createTasksDatabase(self):
        self._cursor.execute(f"CREATE DATABASE {self._config.database}")

    def __checkDatabaseExists(self):
        self._cursor.execute("SHOW DATABASES")
        databases = [result[0] for result in self._cursor.fetchall()]
        return self._config.database in databases

    def __switchToTaksDatabase(self):
        self._cursor.execute(f"USE {self._config.database}")

    # TODO: Use schema validation using the Task type
    # TODO: Can MySQL use enum for status?
    def __createTasksTable(self):
        id = "id INT AUTO_INCREMENT PRIMARY KEY"
        title = "title VARCHAR(255) NOT NULL"
        description = "description TEXT"
        date = "date TIMESTAMP"
        start_time = "start_time TIMESTAMP"
        end_time = "end_time TIMESTAMP"
        goal = "goal VARCHAR(255)"
        status = "status VARCHAR(50) NOT NULL"
        schema = ", ".join(
            [id, title, description, date, start_time, end_time, goal, status]
        )

        self._cursor.execute(f"CREATE TABLE {self._config.table} ({schema})")

    def __checkTableExists(self):
        self._cursor.execute("SHOW TABLES")
        tables = [result[0] for result in self._cursor.fetchall()]
        return self._config.table in tables

    def __del__(self):
        logging.info("Closing database connection")
        self._mydb.close()

    def getTaskByID(self, id: int) -> Task:
        fields = [field.name for field in dataclasses.fields(Task)]

        sql_command = f"SELECT  * FROM {self._config.table} WHERE id={id}"
        self._cursor.execute(sql_command)
        result = self._cursor.fetchall()

        if len(result) != 1:
            logging.warning(
                "Multiple tasks with the same id found. Using the first one"
            )

        logging.debug(result)
        args = dict(zip(fields, result[0]))
        task = Task(**args)  # type: ignore
        return task

    def addTask(self, task: Task) -> int:
        fields = []

        if task.title is not None:
            fields.append(("title", task.title, "%s"))
        if task.description is not None:
            fields.append(("description", task.description, "%s"))
        if task.date is not None:
            fields.append(("date", task.date, "%s"))
        if task.start_time is not None:
            fields.append(("start_time", task.start_time, "%s"))
        if task.end_time is not None:
            fields.append(("end_time", task.end_time, "%s"))
        if task.goal is not None:
            fields.append(("goal", task.goal, "%s"))
        if task.status is not None:
            fields.append(("status", task.status.name, "%s"))

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

        return id
