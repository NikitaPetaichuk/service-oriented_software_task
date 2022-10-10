from uuid import uuid4
from typing import Dict

import psycopg2

from users_db_commands import UsersDBCommands


class UsersModel:

    def __init__(self, db_host: str, db_port: int, db_user: str, db_password: str, db_name: str):
        self.db_connection = psycopg2.connect(
            host=db_host, port=db_port, user=db_user, password=db_password, dbname=db_name
        )
        with self.db_connection.cursor() as cursor:
            cursor.execute(UsersDBCommands.CREATE_USERS_TABLE_COMMAND)
        self.db_connection.commit()

    @staticmethod
    def is_user_data_valid(user_data: Dict) -> bool:
        got_all_fields = "name" in user_data and \
                         "surname" in user_data and \
                         "age" in user_data
        if not got_all_fields:
            return False
        if len(user_data) != 3:
            return False
        return \
            type(user_data["name"]) is str and \
            type(user_data["surname"]) is str and \
            type(user_data["age"]) is int

    def _check_user_existence(self, user_id: str) -> bool:
        with self.db_connection.cursor() as cursor:
            cursor.execute(UsersDBCommands.GET_USER_COMMAND, (user_id,))
            if cursor.rowcount == 0:
                return False
            return True

    def set_user_data(self, user_data: Dict, user_id: str | None = None) -> str | None:
        if not user_id:
            user_id = str(uuid4())
            command = UsersDBCommands.INSERT_USER_COMMAND
            value_tuple = (user_id, user_data["name"], user_data["surname"], user_data["age"])
        elif not self._check_user_existence(user_id):
            return None
        else:
            command = UsersDBCommands.UPDATE_USER_COMMAND
            value_tuple = (user_data["name"], user_data["surname"], user_data["age"], user_id)
        with self.db_connection.cursor() as cursor:
            cursor.execute(command, value_tuple)
        self.db_connection.commit()
        return user_id

    def get_user_data(self, user_id: str) -> Dict | None:
        with self.db_connection.cursor() as cursor:
            cursor.execute(UsersDBCommands.GET_USER_COMMAND, (user_id,))
            if cursor.rowcount == 0:
                return None
            user_row = cursor.fetchone()
            return {
                "name": user_row[1],
                "surname": user_row[2],
                "age": user_row[3]
            }

    def delete_user_data(self, user_id: str) -> bool:
        if self._check_user_existence(user_id):
            with self.db_connection.cursor() as cursor:
                cursor.execute(UsersDBCommands.DELETE_USER_COMMAND, (user_id,))
            self.db_connection.commit()
            return True
        return False
