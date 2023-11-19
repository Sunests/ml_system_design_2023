import psycopg2 as pg


class DatabaseWorker:
	def __init__(self, database_name='ml-third_party_service_copy', user='postgres', password='4444555556'):
		self.connection = pg.connect(dbname=database_name, user=user, password=password, host='localhost')
		self.cursor = self.connection.cursor()

	def __del__(self):
		self.connection.close()
	def insert(self, query):
		self.cursor.execute(query)
		self.connection.commit()
		print(self.cursor.fetchall())
		return
	def update(self, query):
		self.cursor.execute(query)
		self.connection.commit()
		#print(self.cursor.fetchall())
		return
	def select(self, query):
		self.cursor.execute(query)
		return self.cursor.fetchall()
	def delete(self, query):
		self.cursor.execute(query)
		self.connection.commit()
		print(self.cursor.fetchall())
		return
