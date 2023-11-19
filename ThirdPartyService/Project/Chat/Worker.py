import os
import openai
from Project.Database import Manager as database_manager
import random


class ChatWorker:
	def __init__(self):
		self.db = database_manager.DatabaseManager()
		self.client = openai.OpenAI(api_key=os.getenv("CHATGPT_API_KEY"))
		self.role="user" #system, assistant

	# def analyseDatabase(self, product):
	# 	print()
	def getResponse(self, request, role="system", context=""):
		messages = [
			{"role": role, "content": ""},
			{"role": "user", "content": request}
		]
		response = self.client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
		return response.choices[0].message.content

	def getResponseCustom(self, product, request):
		response=self.getResponse((f'Если предложение "{request}" похоже на какое-нибудь предложение из '
				            'списка предложений, напиши первой строкой только похожее предложения в списке, а второй '
				            f'строкой только свой ответ на это предложение в контексте продукта {product}. В случае, если похожего '
				            f'предложения нет в списке, но на него можно ответить в контексте продукта {product}, напиши только '
				            'свой ответ на это предложение. Во всех остальных случаях напиши только слово "НЕТ".\n\n'
				            'Список предложений:'+self.db.request_texts), "system", "You will be provided with intructions which you need to execute correctly.")
		lines = response.split('\n')
		if lines[0].upper() != "НЕТ":
			if len(lines) == 1:
				if request.startswith('"') and request.endswith('"'):
					self.db.addRequest(product, request)
				else:
					self.db.addRequest(product, '"'+request+'"')
			else:
				if lines[0].startswith('"') and lines[0].endswith('"'):
					self.db.updateRequestStatistics(product, lines[0])
				else:
					self.db.updateRequestStatistics(product, '"'+lines[0]+'"')
				lines=lines[1]
		else:
			return "Извините, информация по этому запросу о данном продукте недоступна."
		return lines
	def getResponseMostPopular(self, product):
		limit=5
		if random.random():
			requests=self.db.getMostPopularRequests(limit, product)
		else:
			requests = self.db.getMostPopularRequests(limit, "")
		return self.getResponse('Ответь на вопрос "'+requests[random.randint(0, limit)]+f'" по отношению к продукту {product}')
	def getResponsePromotional(self):
		limit=5
		products=self.db.getLowSellingProducts(limit)
		return self.getResponse((f'Напиши красочную рекламу для продукта {products[random.randint(0, limit)]}'))
	def getResponseSimilarProduct(self, product):
		limit = 5
		product_list="Product list:"
		for row in self.db.getSimilarProducts(limit, product):
			product_list+=f'\n{row}'
		return self.getResponse(product_list, context=('You are an assistant whose goal is to choose the product from the list '
								                f'of products which is the most limilar to {product} and compose an '
								                'promotional offer for chosen product'))
