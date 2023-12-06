# -*- coding: utf-8 -*-
import psycopg2 as pg


class Database_client:
    def __init__(self, database_name='ml_db', user='admin', password='1234'):
        self.connection = pg.connect(dbname=database_name, user=user, password=password, host='ml_db')
        self.cursor = self.connection.cursor()  #ml_db

    def __del__(self):
        self.connection.close()

    def get_energy(self, fruit_name):
        query = f"SELECT bzu FROM energy WHERE class_name = '{fruit_name}'"
        result = self._db_select(query)

        if result:
            return result[0][0]  # Возвращаем значение БЖУ
        else:
            return f"Информация о БЖУ для {fruit_name} не найдена"

    def get_praise(self, fruit_name):
        query = f"SELECT price FROM prices WHERE class_name = '{fruit_name}'"
        result = self._db_select(query)

        if result:
            return str(result[0][0])  # Возвращаем цену
        else:
            return f"Информация о цене для {fruit_name} не найдена"

    def _db_select(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()