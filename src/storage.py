from src.models.receipt_model import receipt_model
from src.models.receipt_model_unit import receipt_model_unit

class storage_repository:
    def __init__(self):
        self.recipes = {}
        self.recipes["recipes"] = []  # Список для хранения рецептов

    def add_recipe(self, recipe):
        self.recipes["recipes"].append(recipe)

    def add_items(self, name,  items):
        self.recipes[name] = items

    def get_data(self):
        return self.recipes # todo other models

    def dump(self):
        if not self.recipes:
            print("Нет сохраненных рецептов.")
        else:
            for index, recipe in enumerate(self.recipes, start=1):
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
    