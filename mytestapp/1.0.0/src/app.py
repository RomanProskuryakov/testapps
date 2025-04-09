import json
import psycopg2
from psycopg2 import sql

from walkoff_app_sdk.app_base import AppBase

class MyTestApp(AppBase):
    __version__ = "1.0.0"
    app_name = "mytestapp"  # this needs to match "name" in api.yaml

    def __init__(self, redis, logger, console_logger=None):
        """
        Each app should have this __init__ to set up Redis and logging.
        :param redis:
        :param logger:
        :param console_logger:
        """
        super().__init__(redis, logger, console_logger)
    
    def connect_to_database(self, host, port, dbname, user, password):
        try:
            connection = psycopg2.connect(
                host=host,
                port=port,
                dbname=dbname,
                user=user,
                password=password
            )
            print("Успешное подключение к базе данных!")
            return connection
        except psycopg2.OperationalError as e:
            print(f"Ошибка подключения к базе данных: {e}")
            print("Проверьте параметры подключения (хост, порт, имя базы данных, логин, пароль).")
            return None
        except Exception as e:
            print(f"Неожиданная ошибка при подключении: {e}")
            return None

    def execute_query(self, connection, query):
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                return result
        except psycopg2.DatabaseError as e:
            print(f"Ошибка при выполнении запроса: {e}")
            print("Проверьте корректность SQL-запроса.")
            return None
        except Exception as e:
            print(f"Неожиданная ошибка при выполнении запроса: {e}")
            return None

    def query_database(self, username, password, host, port, database, query):
        self.connection = self.connect_to_database(host, port, database, username, password)
        if not self.connection:
            print("Программа завершена из-за ошибки подключения.")
            return
        result = self.execute_query(self.connection, query)
        if result is not None:
            print("Результаты запроса:")
            for row in result:
                print(row)
            print(len(result))
        else:
            print("Не удалось получить результаты запроса.")
        try:
            self.connection.close()
            print("Соединение закрыто.")
        except Exception as e:
            print(f"Ошибка при закрытии соединения: {e}")
        return (json.dumps(len(result)))    

if __name__ == "__main__":
    MyTestApp.run()