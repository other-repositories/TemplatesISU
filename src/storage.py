from src.models.receipt_model import receipt_model
from src.models.receipt_model_unit import receipt_model_unit
from src.errors.error_utils import error_proxy, argument_exception, operation_exception

import os
import json
import pickle

class storage_repository:
    def __init__(self):
        self.data_storage = {}
        self.data_storage["data_storage"] = []  # Список для хранения рецептов

    def add_recipe(self, recipe):
        self.data_storage["recipes"].append(recipe)

    def add_items(self, name,  items):
        self.data_storage[name] = items

    def get_data(self):
        return self.data_storage # todo other models

    def load(self):
        try:
            with open('storage.json', "r",encoding='utf-8') as read_file:
                pickle.dump(self.data_storage, read_file)
        except Exception as ex:
            raise operation_exception("Ошибка при чтении данных. Файл storage.json")
        
        
    def save(self):
        try:
            with open('storage.json', "w",encoding='utf-8') as write_file:
                self.data_storage = pickle.load(write_file)
        except Exception as ex:
            raise operation_exception("Ошибка при записи файла storage.json")


    def dump(self):
        if not self.data_storage:
            print("Нет сохраненных рецептов.")
        else:
            for index, recipe in enumerate(self.data_storage, start=1):
                print(f"Рецепт {index}:")
                self.print_recipe(recipe)
                print("-" * 40)

    @staticmethod
    def print_recipe(recipe):
        details = recipe.get_receipt_details()  # Получаем детали рецепта
        print(f"Название: {details['title']}")
        print(f"Ингредиенты:")
        for ingredient in details.get('ingredients', []):
            print(f"  - {ingredient['name']}: {ingredient['size']},{ingredient['unit']}")
        print(details["extra"])
        for ingredient in details['full_desc']:
            print(ingredient)
    