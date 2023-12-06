# -*- coding: utf-8 -*-
import psycopg2 as pg


class Database_client:
    def __init__(self):
        def __init__(self, database_name='ml_db', user='admin', password='1234'):
            self.connection = pg.connect(dbname=database_name, user=user, password=password, host='localhost')
            self.cursor = self.connection.cursor()

    def get_energy(self, fruit_name):
        print(f"Запрос энергетической ценности для {fruit_name}")

    def get_praise(self, fruit_name):
        print(f"Запрос цены в рублях для {fruit_name}")