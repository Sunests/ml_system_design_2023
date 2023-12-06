# -*- coding: utf-8 -*-
from Database.Database_client import Database_client
from Chat.GPT_client import GPT_client


class Product_button_parser:
    def __init__(self):
        self.database_client = Database_client()
        self.gpt_client = GPT_client()
        self.button_mapping = {
            "button1": self.database_client.get_energy,
            "button2": self.database_client.get_praise,
            "button3": self.gpt_client.random_fact,
        }

    def process_string(self, input_string):
        # Разделение строки на два параметра
        button, fruit_name = self._extract_params(input_string)

        # Вызов соответствующего метода из словаря
        if button in self.button_mapping:
            self.button_mapping[button](fruit_name)
        else:
            print("Неподдерживаемая операция")

    def _extract_params(self, input_string):
        # Пример разделения строки на два параметра
        parts = input_string.split(" ", 1)
        button = parts[0]
        fruit_name = parts[1] if len(parts) > 1 else None
        return button, fruit_name


input_string = "button1 (button2, button3) название фрукта (артбуз, яблоко)"
