import random
from api_manager.Project.Chat import Worker as worker


class ChatManager:
	def __init__(self):
		self.worker=worker.ChatWorker()

	def getRandomInfo(self, product):   # Called if no request provided by user
		number = random.randint(0, 2)
		if number == 0:
			return self.worker.getResponseMostPopular(product)
		elif number==1:
			return self.worker.getResponseSimilarProduct(product)
		elif number == 2:
			return self.worker.getResponsePromotional()
		else:
			pass
	def getCustomInfo(self, product, request):
		return self.worker.getResponseCustom(product, request)
	def getProductInfo(self, product):  #Button 1
		return self.worker.getResponse((f'Опиши {product} по следующим параметрам: '
		                                f'Популярность '
		                                f'Средняя цена '
		                                f'Калорийность '
		                                f'Полеза или вред для здоровья '))

	def getProductFact(self, product):  #Button 2
		return self.worker.getResponse((f'Расскажи интересный факт о {product}'))
