import sqlite3
from task import Task


class TasksDatabase(object):

    def __init__(self, path: str):

        try:
            self.base_connection = sqlite3.connect(path)
        except sqlite3.DatabaseError:
            print("ERROR! Wrong path")
        else:
            self.base_cursor = self.base_connection.cursor()

    @staticmethod
    def get_sql_response(cursor: sqlite3.Cursor,
                         sql_request: str,
                         arguments: tuple = ()) -> list:
        """
        :param cursor: current database sqlite3 cursor
        :param sql_request: string sql command
        :param arguments: arguments that are passed to the request
        :return: list with responses
        """

        if len(arguments) > 0:
            sql_response = cursor.execute(sql_request, arguments)
        else:
            sql_response = cursor.execute(sql_request)

        return sql_response.fetchall()

    def find_tasks_by(self, **parameter) -> list:
        """
        find all tasks with current number or name or tag
        Example: find_tasks_by(name="Найти") return list with
        all "task" objects with current substring "Найти" in the name field
        :param parameter: number: int, name: str, tag: str
        :return: list of tasks
        """

        sql_requests = {
            "tag": "SELECT * FROM tasks WHERE tags LIKE ?",
            "number": "SELECT * FROM tasks WHERE number=?",
            "name": "SELECT * FROM tasks WHERE name LIKE ?"
        }

        parameter_name, parameter_value = tuple(parameter.items())[0]

        if parameter_name is not "number":
            parameter_value = '%' + parameter_value + '%'

        sql_response = self.get_sql_response(self.base_cursor,
                                             sql_requests[parameter_name],
                                             (parameter_value,)
                                             )
        tasks = []
        if len(sql_response) > 0:
            for args in sql_response:
                tasks.append(Task(*args))

        return tasks

    def add_task(self, task: Task):
        """
        Add a new task in database
        :param task: new task object
        :return: None
        """

        max_index = self.base_cursor.execute("SELECT MAX(ind) FROM tasks").fetchone()[0]
        sql_request = f"INSERT INTO tasks VALUES (?, ?, ?)"

        self.base_cursor.execute(
            sql_request,
            (max_index+1, task.name, task.url,)
        )
        self.base_connection.commit()

    def close(self):
        """
        Close database connection
        :return: None
        """

        self.base_connection.close()