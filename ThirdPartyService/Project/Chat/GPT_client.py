# -*- coding: utf-8 -*-
import openai
import os

class GPT_client:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv("CHATGPT_API_KEY"))
        self.role = "user"

    def random_fact(self, fruit_name):
        print(f"Запрос случайного факта для {fruit_name}")
