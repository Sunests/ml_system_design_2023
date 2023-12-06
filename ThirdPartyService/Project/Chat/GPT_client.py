# -*- coding: utf-8 -*-
import openai
from dotenv import load_dotenv
import os

class GPT_client:
    def __init__(self):
        load_dotenv()
        self.client = openai.OpenAI(api_key=os.getenv("CHATGPT_API_KEY"))
        self.role = "user"

    def getResponse(self, request, role="system", context=""):
        messages = [
            {"role": role, "content": context},
            {"role": "user", "content": request}
        ]
        try:
            response = self.client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
        except Exception as e:
            return "Превышен лимит запросов в минуту."
        return response.choices[0].message.content

    def random_fact(self, fruit_name):
        print(f"Запрос случайного факта для {fruit_name}")
        return self.getResponse((f'Напиши случайный интересный факт для продукта {fruit_name}'))


