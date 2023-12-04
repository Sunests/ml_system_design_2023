from Project.Database import Worker as worker

class DatabaseManager:
	def __init__(self):
		self.worker=worker.DatabaseWorker()
		self.products=[]
		self.request_texts=""
		self.updateProducts()
		self.updateRequestTexts()
	def updateProducts(self):
		data=self.worker.select('SELECT name FROM "Product"')
		for row in data:
			self.products.append(row)
	def updateRequestTexts(self):
		data=self.worker.select('SELECT text FROM "Request"')
		self.request_texts = ""
		for row in data:
			self.request_texts+='\n'+row[0]
	def addRequest(self, product, request):
		query=self.worker.insert('INSERT INTO "Request" '
		                          '(text, count_received) VALUES '
		                          f'(\'{request}\', 1);')
		request_id = self.worker.select('SELECT id FROM "Request" '
		                                f'WHERE text=\'{request}\'')
		product_id = self.worker.select('SELECT id FROM "Product" '
		                                f'WHERE name=\'{product}\'')
		query = self.worker.insert('INSERT INTO "Product_Request "'
		                            '(text, count_received) VALUES '
		                            f'(\'{request}\', 1);')
		self.updateRequestTexts()
	def updateRequestStatistics(self, product, request):
		query=self.worker.update('UPDATE "Request" SET '
		                         'count_received=count_received+1 '
		                         f'WHERE text=\'{request}\'')
		request_id=self.worker.select('SELECT id FROM "Request" '
		                              f'WHERE text=\'{request}\'')
		request_id=request_id.pop()[0]
		product_id = self.worker.select('SELECT id FROM "Product" '
		                                f'WHERE name=\'{product}\'')
		product_id=product_id.pop()[0]
		query = self.worker.update('UPDATE "Product_Request" SET '
		                           'count_received=count_received+1 '
		                           f'WHERE request_id={request_id} AND product_id={product_id}')
	def getMostPopularRequests(self, limit, product=""):
		if product=="":
			query=self.worker.select('SELECT text FROM "Request" '
		                            'ORDER BY "Request".count_received '
		                            f'LIMIT {limit}')
		else:
			query = self.worker.select('SELECT "Request".text FROM "Request" '
			                           f'INNER JOIN "Product" ON "Product".name=\'{product}\' '
			                           'INNER JOIN "Product_Request" ON "Product".id="Product_Request".product_id '
			                           'WHERE "Request".id="Product_Request".request_id '
			                           'ORDER BY "Request".count_received '
			                           'LIMIT 5')
		return query
	def getLowSellingProducts(self, limit):
		query = self.worker.select('SELECT name FROM "Product" '
		                           'ORDER BY random() '
		                           f'LIMIT {limit}')
		return query
	def getSimilarProducts(self, limit, product):
		product_type=self.worker.select('SELECT type FROM "Product" '
		                        f'WHERE name=\'{product}\'')[0][0]
		query = self.worker.select('SELECT name FROM "Product" '
		                           f'WHERE name!=\'{product}\' AND type=\'{product_type}\''
		                           'ORDER BY random() '
		                           f'LIMIT {limit}')
		return query
